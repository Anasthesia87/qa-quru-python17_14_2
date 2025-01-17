"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""

import pytest
from selene import browser, by, be
from selenium import webdriver


@pytest.fixture(params=[(1920, 1080), (1366, 768), (3840, 2160), (720, 1280)],
                ids=['1920x1080', '1366x768', '3840x2160', 'HD'])
def settings_browser(request):
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options
    browser.config.base_url = 'https://github.com'
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height

    browser_type = 'desktop' if int(width) > 1080 else 'mobile'

    yield browser_type


def test_github_desktop(settings_browser):
    if settings_browser == 'mobile':
        pytest.skip(reason='Разрешение экрана для мобильной версии')
    browser.open('/')

    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)


def test_github_mobile_only_hd(settings_browser):
    if settings_browser == 'desktop':
        pytest.skip(reason='Разрешение экрана для десктопной версии')
    browser.open('/')

    browser.element("[class='Button-content']").click()
    browser.element(by.text("Sign up")).click()

    browser.element('#login').should(be.visible)
