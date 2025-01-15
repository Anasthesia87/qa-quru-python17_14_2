"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""
import pytest
from selene import browser, by, be
from selenium import webdriver


@pytest.fixture(params=[(1920, 1080), (1366, 768), (3840, 2160), (1080, 1920), (1440, 2960), (720, 1280)])
def settings_browser(request):
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options
    browser.config.base_url = 'https://github.com'
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height


@pytest.mark.parametrize('settings_browser', [(1920, 1080), (1366, 768), (3840, 2160)],
                         ids=['1920x1080', '1366x768', '3840x2160'],
                         indirect=True)
def test_github_desktop(settings_browser):
    browser.open('/')

    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)


@pytest.mark.parametrize('settings_browser', [(1080, 1920), (1440, 2960)],
                         ids=['FHD', 'QHD'],
                         indirect=True)
def test_github_mobile(settings_browser):
    browser.open('/')

    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)


@pytest.mark.parametrize('settings_browser', [(720, 1280)],
                         ids=['HD'],
                         indirect=True)
def test_github_mobile_only_hd(settings_browser):
    browser.open('/')

    browser.element("[class='Button-content']").click()
    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)
