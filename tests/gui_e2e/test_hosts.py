#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import re
from urllib.parse import quote_plus

from faker import Faker
from playwright.sync_api import expect

from tests.testlib.playwright.pom.dashboard import LoginPage
from tests.testlib.playwright.timeouts import TIMEOUT_ACTIVATE_CHANGES_MS


class TestHost:
    def __init__(self) -> None:
        self.name: str = f"test_host_{Faker().first_name()}"
        self.ip: str = "127.0.0.1"


class TestHosts:
    # Text of popup menus seen on GUI
    popup_menus: list[str] = [
        "Host",
        "Display",
        "Help",
    ]

    # Text of links seen on GUI
    links: list[str] = [
        r"Save & run service discovery",
        r"Save & view folder",
        r"Save & run connection tests",
        r"Update site DNS cache",
    ]

    properties: list[str] = [
        r"Monitoring agents",
        r"Custom attributes",
        r"Management board",
        r"Creation / Locking",
    ]

    def test_navigate_to_host_properties(self, logged_in_page: LoginPage) -> None:
        # Setup
        host = TestHost()
        self._create_host(logged_in_page, host)
        # Test-body
        logged_in_page.main_menu.setup_hosts.click()
        # - to host-properties
        url_pattern: str = quote_plus(f"wato.py?folder=&host={host.name}&mode=edit_host")
        logged_in_page.main_area.get_text(host.name).click()
        # - wait until the whole page is loaded
        logged_in_page.page.wait_for_url(
            url=re.compile(url_pattern), wait_until="load", timeout=TIMEOUT_ACTIVATE_CHANGES_MS
        )

        # - sanity checks
        for link in self.popup_menus + self.links + self.properties:
            locator = logged_in_page.main_area.get_text(text=link, first=False)
            expect(locator).to_have_count(1)

        # - check absence of errors and warnings
        expect(logged_in_page.main_area.locator("div.error")).to_have_count(0)
        expect(logged_in_page.main_area.locator("div.warning")).to_have_count(0)

        # Cleanup
        self._delete_host(logged_in_page, host)

    def test_create_and_delete_a_host(self, logged_in_page: LoginPage, is_chromium: bool) -> None:
        """Creates a host and deletes it afterwards. Calling order of static methods
        is therefore essential!
        """
        host = TestHost()
        self._create_host(logged_in_page, host)

        logged_in_page.main_menu.monitor_all_hosts.click()
        logged_in_page.select_host(host.name)

        self._delete_host(logged_in_page, host)

    def test_reschedule(self, logged_in_page: LoginPage, is_chromium: bool) -> None:
        """reschedules a check"""
        host = TestHost()
        self._create_host(logged_in_page, host)

        logged_in_page.main_menu.monitor_all_hosts.click()
        logged_in_page.select_host(host.name)

        # Use the Check_MK Service. It is always there and the first.
        # There are two Services containing "Check_MK", using the first
        logged_in_page.main_area.locator(
            "tr.data:has-text('Check_MK') >> nth=0 >> img[title='Open the action menu']"
        ).click()
        logged_in_page.main_area.locator("div#popup_menu >> a:has-text('Reschedule check')").click()
        # In case of a success the page is reloaded, therefore the div is hidden,
        # otherwise the div stays open...
        logged_in_page.main_area.locator("div#popup_menu").wait_for(state="hidden")

        self._delete_host(logged_in_page, host)

    @staticmethod
    def _create_host(logged_in_page: LoginPage, host: TestHost) -> None:
        """Creates a host by starting from a logged in page."""
        logged_in_page.main_menu.setup_hosts.click()
        logged_in_page.main_area.get_suggestion("Add host").click()

        logged_in_page.main_area.get_input("host").fill(host.name)
        logged_in_page.main_area.get_attribute_label("ipaddress").click()
        logged_in_page.main_area.get_input("ipaddress").fill(host.ip)

        logged_in_page.main_area.get_suggestion("Save & run service discovery").click()
        logged_in_page.main_area.get_element_including_texts(
            element_id="changes_info", texts=["1", "change"]
        ).click()

        logged_in_page.activate_selected()
        logged_in_page.expect_success_state()

    @staticmethod
    def _delete_host(logged_in_page: LoginPage, host: TestHost) -> None:
        """Deletes the former created host by starting from a logged in page."""
        logged_in_page.main_menu.setup_hosts.click()

        # click on "delete host" for the given hostname via xpath selector
        logged_in_page.main_area.locator(
            f"div#popup_trigger_host_action_menu_{host.name} >> a,popup_trigger"
        ).click()
        logged_in_page.main_area.locator(
            f"div#popup_trigger_host_action_menu_{host.name} >> div#popup_menu"
        ).wait_for()

        logged_in_page.main_area.get_text("Delete host").click()
        logged_in_page.main_area.locator_via_xpath("button", "Remove").click()

        logged_in_page.main_area.get_element_including_texts(
            element_id="changes_info", texts=["1", "change"]
        ).click()

        logged_in_page.activate_selected()
        logged_in_page.expect_success_state()
