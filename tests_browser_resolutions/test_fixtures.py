"""
Сделайте разные фикстуры для каждого теста, которые выставят размеры окна браузера
"""

import pytest
from selene import browser, by, be
from selenium import webdriver


@pytest.fixture(scope='session')
def settings_browser():
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options
    browser.config.base_url = 'https://github.com'


@pytest.fixture(params=[(1920, 1080), (1366, 768), (3840, 2160)], ids=['1920x1080', '1366x768', '3840x2160'])
def desktop_browser_resolution(settings_browser, request):
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height
    yield
    browser.quit()


@pytest.fixture(params=[(1080, 1920), (1440, 2960)], ids=['FHD', 'QHD'])
def mobile_browser_resolution(settings_browser, request):
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height
    yield
    browser.quit()


@pytest.fixture(params=[(720, 1280)], ids=['HD'])
def mobile_browser_resolution_only_hd(settings_browser, request):
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height
    yield
    browser.quit()


def test_github_desktop(desktop_browser_resolution):
    browser.open('/')

    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)


def test_github_mobile(mobile_browser_resolution):
    browser.open('/')

    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)


def test_github_mobile_only_hd(mobile_browser_resolution_only_hd):
    browser.open('/')

    browser.element("[class='Button-content']").click()
    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)
