# Selenium

Selenium is a powerful framework for automating web applications for testing purposes. It provides a portable software testing framework for web applications across different browsers and platforms.

## Installation

### Python Setup
```bash
# Install Selenium
pip install selenium

# Install WebDriver Manager (simplifies driver management)
pip install webdriver-manager

# Install additional testing frameworks
pip install pytest pytest-html pytest-xdist
pip install allure-pytest

# Verify installation
python -c "import selenium; print(selenium.__version__)"
```

### Java Setup
```xml
<!-- Maven pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.seleniumhq.selenium</groupId>
        <artifactId>selenium-java</artifactId>
        <version>4.15.0</version>
    </dependency>
    <dependency>
        <groupId>io.github.bonigarcia</groupId>
        <artifactId>webdrivermanager</artifactId>
        <version>5.4.1</version>
    </dependency>
    <dependency>
        <groupId>org.testng</groupId>
        <artifactId>testng</artifactId>
        <version>7.8.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

```gradle
// Gradle build.gradle
dependencies {
    testImplementation 'org.seleniumhq.selenium:selenium-java:4.15.0'
    testImplementation 'io.github.bonigarcia:webdrivermanager:5.4.1'
    testImplementation 'org.testng:testng:7.8.0'
}
```

### JavaScript/Node.js Setup
```bash
# Install Selenium WebDriver
npm install selenium-webdriver

# Install test frameworks
npm install mocha chai
npm install jest
npm install webdriverio

# Install browser drivers
npm install chromedriver geckodriver

# Verify installation
node -e "console.log(require('selenium-webdriver/package.json').version)"
```

### Docker
```dockerfile
# Dockerfile for Selenium Grid
FROM selenium/standalone-chrome:latest

# Add test files
COPY tests/ /tests/
COPY package.json /app/
WORKDIR /app

# Install dependencies
RUN npm install

# Run tests
CMD ["npm", "test"]
```

```yaml
# docker-compose.yml for Selenium Grid
version: '3.8'
services:
  selenium-hub:
    image: selenium/hub:latest
    container_name: selenium-hub
    ports:
      - "4444:4444"
    environment:
      - GRID_MAX_SESSION=16
      - GRID_BROWSER_TIMEOUT=300
      - GRID_TIMEOUT=300

  chrome:
    image: selenium/node-chrome:latest
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - HUB_HOST=selenium-hub
      - NODE_MAX_INSTANCES=4
      - NODE_MAX_SESSION=4
    scale: 2

  firefox:
    image: selenium/node-firefox:latest
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - HUB_HOST=selenium-hub
      - NODE_MAX_INSTANCES=4
      - NODE_MAX_SESSION=4
    scale: 2
```

## Basic Usage

### Python Example
```python
# basic_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import time

class TestWebApplication:
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Use WebDriverManager to handle driver setup
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
        yield
        
        # Cleanup
        self.driver.quit()
    
    def test_login_functionality(self):
        """Test user login functionality"""
        # Navigate to login page
        self.driver.get("https://example.com/login")
        
        # Find and fill login form
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Enter credentials
        username_field.send_keys("testuser@example.com")
        password_field.send_keys("password123")
        
        # Submit form
        login_button.click()
        
        # Wait for redirect and verify login success
        self.wait.until(EC.url_contains("/dashboard"))
        
        # Verify user is logged in
        user_menu = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-menu"))
        )
        assert user_menu.is_displayed()
        
        # Check welcome message
        welcome_message = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome')]")
        assert "Welcome" in welcome_message.text
    
    def test_search_functionality(self):
        """Test search functionality"""
        self.driver.get("https://example.com")
        
        # Find search box
        search_box = self.wait.until(
            EC.presence_of_element_located((By.NAME, "search"))
        )
        
        # Perform search
        search_term = "selenium automation"
        search_box.send_keys(search_term)
        search_box.submit()
        
        # Wait for results
        results = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-result"))
        )
        
        # Verify results
        assert len(results) > 0
        assert search_term.lower() in self.driver.page_source.lower()
    
    def test_form_validation(self):
        """Test form validation"""
        self.driver.get("https://example.com/contact")
        
        # Find form elements
        name_field = self.driver.find_element(By.ID, "name")
        email_field = self.driver.find_element(By.ID, "email")
        message_field = self.driver.find_element(By.ID, "message")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Submit empty form
        submit_button.click()
        
        # Check for validation errors
        error_messages = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "error-message"))
        )
        assert len(error_messages) >= 3  # Name, email, message required
        
        # Fill form with valid data
        name_field.send_keys("John Doe")
        email_field.send_keys("john.doe@example.com")
        message_field.send_keys("This is a test message for form validation.")
        
        # Submit valid form
        submit_button.click()
        
        # Verify success message
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "Thank you" in success_message.text
```

### Java Example
```java
// WebTest.java
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.By;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.testng.annotations.*;
import org.testng.Assert;
import io.github.bonigarcia.wdm.WebDriverManager;
import java.time.Duration;

public class WebTest {
    
    private WebDriver driver;
    private WebDriverWait wait;
    
    @BeforeMethod
    public void setUp() {
        // Setup WebDriver using WebDriverManager
        WebDriverManager.chromedriver().setup();
        
        // Configure Chrome options
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--disable-gpu");
        options.addArguments("--window-size=1920,1080");
        
        driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }
    
    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
    
    @Test
    public void testUserRegistration() {
        // Navigate to registration page
        driver.get("https://example.com/register");
        
        // Fill registration form
        WebElement firstNameField = wait.until(
            ExpectedConditions.presenceOfElementLocated(By.id("firstName"))
        );
        WebElement lastNameField = driver.findElement(By.id("lastName"));
        WebElement emailField = driver.findElement(By.id("email"));
        WebElement passwordField = driver.findElement(By.id("password"));
        WebElement confirmPasswordField = driver.findElement(By.id("confirmPassword"));
        WebElement submitButton = driver.findElement(By.cssSelector("button[type='submit']"));
        
        // Enter user data
        firstNameField.sendKeys("John");
        lastNameField.sendKeys("Doe");
        emailField.sendKeys("john.doe" + System.currentTimeMillis() + "@example.com");
        passwordField.sendKeys("SecurePassword123!");
        confirmPasswordField.sendKeys("SecurePassword123!");
        
        // Submit form
        submitButton.click();
        
        // Verify registration success
        WebElement successMessage = wait.until(
            ExpectedConditions.presenceOfElementLocated(By.className("registration-success"))
        );
        Assert.assertTrue(successMessage.isDisplayed());
        Assert.assertTrue(successMessage.getText().contains("Registration successful"));
    }
    
    @Test
    public void testProductCatalog() {
        driver.get("https://example.com/products");
        
        // Wait for products to load
        wait.until(ExpectedConditions.presenceOfElementLocated(By.className("product-grid")));
        
        // Find all product cards
        var products = driver.findElements(By.className("product-card"));
        Assert.assertTrue(products.size() > 0, "No products found");
        
        // Click on first product
        products.get(0).click();
        
        // Verify product details page
        wait.until(ExpectedConditions.urlContains("/products/"));
        
        WebElement productTitle = wait.until(
            ExpectedConditions.presenceOfElementLocated(By.className("product-title"))
        );
        WebElement productPrice = driver.findElement(By.className("product-price"));
        WebElement addToCartButton = driver.findElement(By.className("add-to-cart"));
        
        Assert.assertTrue(productTitle.isDisplayed());
        Assert.assertTrue(productPrice.isDisplayed());
        Assert.assertTrue(addToCartButton.isEnabled());
        
        // Add to cart
        addToCartButton.click();
        
        // Verify item added to cart
        WebElement cartCounter = wait.until(
            ExpectedConditions.presenceOfElementLocated(By.className("cart-counter"))
        );
        Assert.assertEquals(cartCounter.getText(), "1");
    }
    
    @Test
    public void testResponsiveDesign() {
        driver.get("https://example.com");
        
        // Test desktop view
        driver.manage().window().setSize(new org.openqa.selenium.Dimension(1920, 1080));
        WebElement desktopMenu = driver.findElement(By.className("desktop-menu"));
        Assert.assertTrue(desktopMenu.isDisplayed());
        
        // Test tablet view
        driver.manage().window().setSize(new org.openqa.selenium.Dimension(768, 1024));
        wait.until(ExpectedConditions.invisibilityOf(desktopMenu));
        
        // Test mobile view
        driver.manage().window().setSize(new org.openqa.selenium.Dimension(375, 667));
        WebElement mobileMenuButton = wait.until(
            ExpectedConditions.presenceOfElementLocated(By.className("mobile-menu-button"))
        );
        Assert.assertTrue(mobileMenuButton.isDisplayed());
        
        // Test mobile menu functionality
        mobileMenuButton.click();
        WebElement mobileMenu = wait.until(
            ExpectedConditions.visibilityOfElementLocated(By.className("mobile-menu"))
        );
        Assert.assertTrue(mobileMenu.isDisplayed());
    }
}
```

### JavaScript Example
```javascript
// test.js
const { Builder, By, Key, until } = require('selenium-webdriver');
const { Options } = require('selenium-webdriver/chrome');
const assert = require('assert');

describe('Web Application Tests', function() {
    let driver;
    
    this.timeout(30000);
    
    beforeEach(async function() {
        const options = new Options();
        options.addArguments('--no-sandbox');
        options.addArguments('--disable-dev-shm-usage');
        options.addArguments('--disable-gpu');
        options.addArguments('--window-size=1920,1080');
        
        driver = await new Builder()
            .forBrowser('chrome')
            .setChromeOptions(options)
            .build();
        
        await driver.manage().setTimeouts({ implicit: 10000 });
    });
    
    afterEach(async function() {
        if (driver) {
            await driver.quit();
        }
    });
    
    it('should handle dynamic content loading', async function() {
        await driver.get('https://example.com/dynamic');
        
        // Click load more button
        const loadMoreButton = await driver.findElement(By.id('load-more'));
        await loadMoreButton.click();
        
        // Wait for new content to load
        await driver.wait(until.elementLocated(By.className('dynamic-content')), 10000);
        
        // Verify content is loaded
        const dynamicElements = await driver.findElements(By.className('dynamic-item'));
        assert(dynamicElements.length > 0, 'Dynamic content not loaded');
        
        // Verify loading indicator is hidden
        const loadingIndicator = await driver.findElement(By.id('loading'));
        const isDisplayed = await loadingIndicator.isDisplayed();
        assert(!isDisplayed, 'Loading indicator should be hidden');
    });
    
    it('should handle file upload', async function() {
        await driver.get('https://example.com/upload');
        
        // Find file input
        const fileInput = await driver.findElement(By.css('input[type="file"]'));
        
        // Upload file (requires local file path)
        const filePath = require('path').resolve(__dirname, 'test-file.txt');
        await fileInput.sendKeys(filePath);
        
        // Submit upload
        const uploadButton = await driver.findElement(By.id('upload-button'));
        await uploadButton.click();
        
        // Wait for upload completion
        const successMessage = await driver.wait(
            until.elementLocated(By.className('upload-success')),
            15000
        );
        
        const messageText = await successMessage.getText();
        assert(messageText.includes('Upload successful'), 'Upload failed');
    });
    
    it('should handle multiple windows', async function() {
        await driver.get('https://example.com');
        
        const originalWindow = await driver.getWindowHandle();
        
        // Click link that opens new window
        const newWindowLink = await driver.findElement(By.id('open-new-window'));
        await newWindowLink.click();
        
        // Wait for new window
        await driver.wait(async () => {
            const handles = await driver.getAllWindowHandles();
            return handles.length === 2;
        }, 10000);
        
        // Switch to new window
        const windows = await driver.getAllWindowHandles();
        const newWindow = windows.find(handle => handle !== originalWindow);
        await driver.switchTo().window(newWindow);
        
        // Verify new window content
        await driver.wait(until.titleContains('New Window'), 10000);
        const title = await driver.getTitle();
        assert(title.includes('New Window'), 'Wrong window title');
        
        // Close new window and switch back
        await driver.close();
        await driver.switchTo().window(originalWindow);
        
        // Verify we're back on original window
        const originalTitle = await driver.getTitle();
        assert(!originalTitle.includes('New Window'), 'Not on original window');
    });
    
    it('should handle JavaScript alerts', async function() {
        await driver.get('https://example.com/alerts');
        
        // Test alert
        const alertButton = await driver.findElement(By.id('alert-button'));
        await alertButton.click();
        
        await driver.wait(until.alertIsPresent(), 5000);
        const alert = await driver.switchTo().alert();
        const alertText = await alert.getText();
        assert(alertText.includes('Alert message'), 'Wrong alert text');
        await alert.accept();
        
        // Test confirm dialog
        const confirmButton = await driver.findElement(By.id('confirm-button'));
        await confirmButton.click();
        
        await driver.wait(until.alertIsPresent(), 5000);
        const confirm = await driver.switchTo().alert();
        await confirm.accept();
        
        // Verify confirm result
        const result = await driver.findElement(By.id('confirm-result'));
        const resultText = await result.getText();
        assert(resultText === 'Confirmed', 'Confirm not handled correctly');
    });
});
```

## Page Object Model

### Python Page Object Implementation
```python
# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        return self.find_element(locator).text
    
    def is_element_visible(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    def wait_for_url_to_contain(self, text):
        return self.wait.until(EC.url_contains(text))

# pages/login_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    # Locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/login"
    
    def navigate_to_login(self):
        self.driver.get(self.url)
        return self
    
    def enter_username(self, username):
        self.enter_text(self.USERNAME_FIELD, username)
        return self
    
    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD, password)
        return self
    
    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def click_forgot_password(self):
        self.click_element(self.FORGOT_PASSWORD_LINK)
        return self

# pages/dashboard_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class DashboardPage(BasePage):
    # Locators
    USER_MENU = (By.CLASS_NAME, "user-menu")
    WELCOME_MESSAGE = (By.XPATH, "//h1[contains(text(), 'Welcome')]")
    NAVIGATION_MENU = (By.CLASS_NAME, "nav-menu")
    LOGOUT_BUTTON = (By.ID, "logout")
    PROFILE_LINK = (By.LINK_TEXT, "Profile")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_loaded(self):
        return self.is_element_visible(self.USER_MENU) and \
               self.is_element_visible(self.WELCOME_MESSAGE)
    
    def get_welcome_message(self):
        return self.get_text(self.WELCOME_MESSAGE)
    
    def logout(self):
        self.click_element(self.LOGOUT_BUTTON)
        return self
    
    def go_to_profile(self):
        self.click_element(self.PROFILE_LINK)
        return self

# tests/test_login_with_page_objects.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLoginFlow:
    
    def test_successful_login(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # Navigate to login and perform login
        login_page.navigate_to_login() \
                  .login("testuser@example.com", "password123")
        
        # Verify successful login
        assert dashboard_page.is_loaded()
        assert "Welcome" in dashboard_page.get_welcome_message()
    
    def test_invalid_login(self, driver):
        login_page = LoginPage(driver)
        
        # Attempt login with invalid credentials
        login_page.navigate_to_login() \
                  .login("invalid@example.com", "wrongpassword")
        
        # Verify error is displayed
        assert login_page.is_error_displayed()
        assert "Invalid credentials" in login_page.get_error_message()
    
    def test_forgot_password_flow(self, driver):
        login_page = LoginPage(driver)
        
        # Navigate to login and click forgot password
        login_page.navigate_to_login() \
                  .click_forgot_password()
        
        # Verify redirect to forgot password page
        login_page.wait_for_url_to_contain("/forgot-password")
        assert "forgot-password" in driver.current_url
```

## Test Data Management

### Data-Driven Testing
```python
# data/test_data.py
import json
import csv
from dataclasses import dataclass
from typing import List

@dataclass
class UserData:
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: str

class TestDataManager:
    
    @staticmethod
    def load_users_from_json(file_path: str) -> List[UserData]:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return [UserData(**user) for user in data['users']]
    
    @staticmethod
    def load_users_from_csv(file_path: str) -> List[UserData]:
        users = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(UserData(**row))
        return users
    
    @staticmethod
    def generate_test_user() -> UserData:
        import random
        import string
        
        random_id = ''.join(random.choices(string.digits, k=6))
        return UserData(
            username=f"testuser{random_id}",
            password="TestPass123!",
            email=f"test{random_id}@example.com",
            first_name=f"Test{random_id}",
            last_name="User",
            role="user"
        )

# tests/test_data_driven.py
import pytest
from data.test_data import TestDataManager, UserData

class TestUserRegistration:
    
    @pytest.mark.parametrize("user_data", TestDataManager.load_users_from_json("data/valid_users.json"))
    def test_valid_user_registration(self, driver, user_data: UserData):
        # Use the user_data parameter for test
        registration_page = RegistrationPage(driver)
        registration_page.navigate() \
                        .fill_registration_form(user_data) \
                        .submit()
        
        assert registration_page.is_success_displayed()
    
    @pytest.mark.parametrize("user_data", TestDataManager.load_users_from_json("data/invalid_users.json"))
    def test_invalid_user_registration(self, driver, user_data: UserData):
        registration_page = RegistrationPage(driver)
        registration_page.navigate() \
                        .fill_registration_form(user_data) \
                        .submit()
        
        assert registration_page.is_error_displayed()
    
    def test_random_user_registration(self, driver):
        user_data = TestDataManager.generate_test_user()
        registration_page = RegistrationPage(driver)
        
        registration_page.navigate() \
                        .fill_registration_form(user_data) \
                        .submit()
        
        assert registration_page.is_success_displayed()

# data/valid_users.json
{
  "users": [
    {
      "username": "john_doe",
      "password": "SecurePass123!",
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user"
    },
    {
      "username": "jane_smith",
      "password": "StrongPass456!",
      "email": "jane.smith@example.com", 
      "first_name": "Jane",
      "last_name": "Smith",
      "role": "admin"
    }
  ]
}
```

## Advanced Testing Patterns

### Cross-Browser Testing
```python
# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

@pytest.fixture(params=["chrome", "firefox", "safari"])
def driver(request):
    browser = request.param
    
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser == "safari":
        driver = webdriver.Safari()
    
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def chrome_driver():
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def headless_chrome_driver():
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
```

### Mobile Testing
```python
# mobile_testing.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class MobileTestSetup:
    
    @staticmethod
    def get_mobile_driver(device_name="iPhone 12"):
        mobile_emulation = {
            "deviceName": device_name
        }
        
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        return webdriver.Chrome(options=chrome_options)
    
    @staticmethod
    def get_custom_mobile_driver(width, height, user_agent):
        mobile_emulation = {
            "deviceMetrics": {
                "width": width,
                "height": height,
                "pixelRatio": 2.0
            },
            "userAgent": user_agent
        }
        
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        return webdriver.Chrome(options=chrome_options)

# tests/test_mobile_responsiveness.py
import pytest
from mobile_testing import MobileTestSetup

class TestMobileResponsiveness:
    
    @pytest.mark.parametrize("device", ["iPhone 12", "iPad", "Pixel 5"])
    def test_navigation_on_mobile(self, device):
        driver = MobileTestSetup.get_mobile_driver(device)
        
        try:
            driver.get("https://example.com")
            
            # Test mobile navigation
            menu_button = driver.find_element(By.CLASS_NAME, "mobile-menu-toggle")
            assert menu_button.is_displayed()
            
            menu_button.click()
            
            mobile_menu = driver.find_element(By.CLASS_NAME, "mobile-menu")
            assert mobile_menu.is_displayed()
            
        finally:
            driver.quit()
    
    def test_form_input_on_mobile(self):
        driver = MobileTestSetup.get_mobile_driver("iPhone 12")
        
        try:
            driver.get("https://example.com/contact")
            
            # Test form fields are properly sized for mobile
            name_field = driver.find_element(By.ID, "name")
            email_field = driver.find_element(By.ID, "email")
            
            # Verify fields are accessible
            assert name_field.is_displayed()
            assert email_field.is_displayed()
            
            # Test input
            name_field.send_keys("Test User")
            email_field.send_keys("test@example.com")
            
            # Verify input was accepted
            assert name_field.get_attribute("value") == "Test User"
            assert email_field.get_attribute("value") == "test@example.com"
            
        finally:
            driver.quit()
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Selenium Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'

jobs:
  selenium-tests:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        browser: [chrome, firefox]
        test-suite: [smoke, regression, api]
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
        # Install browser drivers
        pip install webdriver-manager
    
    - name: Setup Chrome
      uses: browser-actions/setup-chrome@latest
    
    - name: Setup Firefox
      uses: browser-actions/setup-firefox@latest
    
    - name: Run Selenium Tests
      run: |
        pytest tests/ \
          --browser=${{ matrix.browser }} \
          --test-suite=${{ matrix.test-suite }} \
          --html=reports/report-${{ matrix.browser }}-${{ matrix.test-suite }}.html \
          --self-contained-html \
          --junit-xml=reports/junit-${{ matrix.browser }}-${{ matrix.test-suite }}.xml \
          --maxfail=5 \
          -v
      env:
        BASE_URL: ${{ secrets.TEST_BASE_URL }}
        TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
        TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
    
    - name: Upload Test Reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-reports-${{ matrix.browser }}-${{ matrix.test-suite }}
        path: reports/
    
    - name: Publish Test Results
      uses: dorny/test-reporter@v1
      if: always()
      with:
        name: Selenium Tests (${{ matrix.browser }}-${{ matrix.test-suite }})
        path: reports/junit-*.xml
        reporter: java-junit
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'safari', 'edge'],
            description: 'Browser to run tests'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'regression', 'full'],
            description: 'Test suite to execute'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run tests in headless mode'
        )
    }
    
    environment {
        PYTHON_ENV = 'selenium-tests'
        BASE_URL = credentials('test-base-url')
        TEST_CREDENTIALS = credentials('test-user-credentials')
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                script {
                    sh '''
                        python3 -m venv ${PYTHON_ENV}
                        source ${PYTHON_ENV}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Install Browser Drivers') {
            steps {
                script {
                    sh '''
                        source ${PYTHON_ENV}/bin/activate
                        
                        # Download and setup drivers
                        python -c "
                        from webdriver_manager.chrome import ChromeDriverManager
                        from webdriver_manager.firefox import GeckoDriverManager
                        ChromeDriverManager().install()
                        GeckoDriverManager().install()
                        "
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    sh """
                        source ${PYTHON_ENV}/bin/activate
                        
                        pytest tests/ \\
                          --browser=${params.BROWSER} \\
                          --test-suite=${params.TEST_SUITE} \\
                          --headless=${params.HEADLESS} \\
                          --html=reports/selenium-report.html \\
                          --self-contained-html \\
                          --junit-xml=reports/junit-results.xml \\
                          --maxfail=10 \\
                          --tb=short \\
                          -v
                    """
                }
            }
        }
        
        stage('Process Results') {
            steps {
                script {
                    // Parse test results
                    sh '''
                        source ${PYTHON_ENV}/bin/activate
                        python scripts/parse_test_results.py reports/junit-results.xml
                    '''
                }
            }
        }
    }
    
    post {
        always {
            // Archive test artifacts
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
            
            // Publish HTML reports
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'selenium-report.html',
                reportName: 'Selenium Test Report'
            ])
            
            // Publish JUnit results
            junit 'reports/junit-results.xml'
            
            // Cleanup
            sh 'rm -rf ${PYTHON_ENV}'
        }
        
        failure {
            emailext(
                subject: "Selenium Tests Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                    Selenium tests failed for browser: ${params.BROWSER}
                    Test suite: ${params.TEST_SUITE}
                    
                    View results: ${env.BUILD_URL}
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

## Performance and Best Practices

### Test Optimization
```python
# utils/test_helpers.py
import time
import functools
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def retry_on_exception(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

class PerformanceHelper:
    
    @staticmethod
    def measure_page_load_time(driver, url):
        start_time = time.time()
        driver.get(url)
        
        # Wait for page to be fully loaded
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        end_time = time.time()
        return end_time - start_time
    
    @staticmethod
    def get_performance_metrics(driver):
        # Get Navigation Timing API metrics
        metrics = driver.execute_script("""
            const perfData = performance.getEntriesByType('navigation')[0];
            return {
                loadTime: perfData.loadEventEnd - perfData.loadEventStart,
                domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                responseTime: perfData.responseEnd - perfData.requestStart,
                renderTime: perfData.loadEventEnd - perfData.responseEnd
            };
        """)
        return metrics
    
    @staticmethod
    def capture_network_logs(driver):
        # Enable logging
        logs = driver.get_log('performance')
        network_logs = []
        
        for log in logs:
            message = json.loads(log['message'])
            if message['message']['method'] in ['Network.responseReceived', 'Network.requestWillBeSent']:
                network_logs.append(message)
        
        return network_logs

# tests/test_performance.py
import pytest
from utils.test_helpers import PerformanceHelper

class TestPerformance:
    
    def test_page_load_performance(self, driver):
        load_time = PerformanceHelper.measure_page_load_time(driver, "https://example.com")
        assert load_time < 5.0, f"Page load time {load_time}s exceeds 5s threshold"
    
    def test_navigation_performance(self, driver):
        driver.get("https://example.com")
        metrics = PerformanceHelper.get_performance_metrics(driver)
        
        assert metrics['loadTime'] < 3000, f"Load time {metrics['loadTime']}ms too high"
        assert metrics['responseTime'] < 2000, f"Response time {metrics['responseTime']}ms too high"
        assert metrics['renderTime'] < 1000, f"Render time {metrics['renderTime']}ms too high"
```

## Reporting and Analytics

### Custom Test Reporting
```python
# reporting/custom_reporter.py
import json
import time
from datetime import datetime
import pytest

class CustomTestReporter:
    
    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        
        if report.when == "call":
            test_result = {
                'test_name': item.name,
                'test_file': str(item.fspath),
                'outcome': report.outcome,
                'duration': report.duration,
                'timestamp': datetime.now().isoformat(),
                'browser': item.config.getoption('--browser', 'unknown'),
                'error_message': str(report.longrepr) if report.failed else None
            }
            
            # Add custom test metadata
            if hasattr(item, 'test_metadata'):
                test_result.update(item.test_metadata)
            
            self.test_results.append(test_result)
    
    def pytest_sessionstart(self, session):
        self.start_time = time.time()
    
    def pytest_sessionfinish(self, session):
        self.end_time = time.time()
        self.generate_report()
    
    def generate_report(self):
        report_data = {
            'summary': {
                'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                'end_time': datetime.fromtimestamp(self.end_time).isoformat(),
                'duration': self.end_time - self.start_time,
                'total_tests': len(self.test_results),
                'passed': len([r for r in self.test_results if r['outcome'] == 'passed']),
                'failed': len([r for r in self.test_results if r['outcome'] == 'failed']),
                'skipped': len([r for r in self.test_results if r['outcome'] == 'skipped'])
            },
            'tests': self.test_results
        }
        
        # Save to file
        with open('reports/custom-test-report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Send to monitoring system (example)
        self.send_metrics_to_monitoring(report_data)
    
    def send_metrics_to_monitoring(self, report_data):
        # Example: Send metrics to external monitoring system
        pass

# pytest plugin registration
def pytest_configure(config):
    config.pluginmanager.register(CustomTestReporter(), "custom_reporter")
```

## Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Selenium WebDriver API](https://www.selenium.dev/documentation/webdriver/)
- [Selenium Grid](https://www.selenium.dev/documentation/grid/)
- [Page Object Model](https://selenium-python.readthedocs.io/page-objects.html)
- [Test Automation Best Practices](https://www.selenium.dev/documentation/test_practices/)
- [Browser Driver Downloads](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)
- [Selenium IDE](https://www.selenium.dev/selenium-ide/)
- [Appium for Mobile Testing](http://appium.io/)
- [Selenium Community](https://www.selenium.dev/support/)
- [WebDriver BiDi](https://w3c.github.io/webdriver-bidi/)