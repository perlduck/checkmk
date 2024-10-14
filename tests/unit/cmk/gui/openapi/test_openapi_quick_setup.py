#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Callable, Sequence

import pytest

from tests.testlib.rest_api_client import ClientRegistry

from cmk.gui.fields.definitions import FOLDER_PATTERN
from cmk.gui.quick_setup.v0_unstable._registry import quick_setup_registry
from cmk.gui.quick_setup.v0_unstable.definitions import UniqueBundleIDStr, UniqueFormSpecIDStr
from cmk.gui.quick_setup.v0_unstable.predefined import recaps, widgets
from cmk.gui.quick_setup.v0_unstable.predefined import validators as qs_validators
from cmk.gui.quick_setup.v0_unstable.setups import QuickSetup, QuickSetupAction, QuickSetupStage
from cmk.gui.quick_setup.v0_unstable.type_defs import (
    GeneralStageErrors,
    ParsedFormData,
    QuickSetupId,
    StageIndex,
)
from cmk.gui.quick_setup.v0_unstable.widgets import (
    FormSpecId,
    FormSpecWrapper,
)
from cmk.gui.watolib.configuration_bundles import ConfigBundleStore

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    FieldSize,
    String,
    validators,
)


def register_quick_setup(
    setup_stages: Sequence[Callable[[], QuickSetupStage]] | None = None,
    load_data: Callable[[str], ParsedFormData | None] = lambda _: None,
) -> None:
    quick_setup_registry.register(
        QuickSetup(
            title="Quick Setup Test",
            id=QuickSetupId("quick_setup_test"),
            stages=setup_stages if setup_stages is not None else [],
            actions=[
                QuickSetupAction(
                    id="save",
                    label="Complete",
                    action=lambda stages, mode, object_id: "http://save/url",
                ),
                QuickSetupAction(
                    id="other_save",
                    label="Complete2: The Sequel",
                    action=lambda stages, mode, object_id: "http://other_save",
                ),
            ],
            load_data=load_data,
        ),
    )


def test_get_quick_setup_mode_guided(clients: ClientRegistry) -> None:
    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                configure_components=[
                    widgets.unique_id_formspec_wrapper(Title("account name")),
                ],
                custom_validators=[],
                recap=[],
                button_label="Next",
            ),
        ],
    )
    resp = clients.QuickSetup.get_overview_mode_or_guided_mode(
        quick_setup_id="quick_setup_test", mode="guided"
    )
    assert len(resp.json["overviews"]) == 1
    assert len(resp.json["stage"]["next_stage_structure"]["components"]) == 1
    assert resp.json["stage"]["next_stage_structure"]["button_label"] == "Next"


def test_validate_retrieve_next(clients: ClientRegistry) -> None:
    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                configure_components=[
                    widgets.unique_id_formspec_wrapper(Title("account name")),
                ],
                custom_validators=[],
                recap=[recaps.recaps_form_spec],
                button_label="Next",
            ),
            lambda: QuickSetupStage(
                title="stage2",
                configure_components=[],
                custom_validators=[],
                recap=[],
                button_label="Next",
            ),
        ],
    )
    resp = clients.QuickSetup.send_stage_retrieve_next(
        quick_setup_id="quick_setup_test",
        stages=[{"form_data": {UniqueFormSpecIDStr: {UniqueBundleIDStr: "test_account_name"}}}],
    )
    assert resp.json["errors"] is None
    assert len(resp.json["stage_recap"]) == 1
    assert resp.json["next_stage_structure"]["button_label"] == "Next"


def _form_spec_extra_validate(
    _quick_setup_id: QuickSetupId, _stage_index: StageIndex, _stages: ParsedFormData
) -> GeneralStageErrors:
    return ["this is a general error", "and another one"]


def test_failing_validate(clients: ClientRegistry) -> None:
    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                configure_components=[
                    widgets.unique_id_formspec_wrapper(Title("account name")),
                ],
                custom_validators=[_form_spec_extra_validate],
                recap=[],
                button_label="Next",
            ),
        ],
    )
    resp = clients.QuickSetup.send_stage_retrieve_next(
        quick_setup_id="quick_setup_test",
        stages=[{"form_data": {UniqueFormSpecIDStr: {UniqueBundleIDStr: 5}}}],
        expect_ok=False,
    )
    resp.assert_status_code(400)
    assert resp.json["errors"] == {
        "formspec_errors": {
            "formspec_unique_id": [
                {
                    "location": [UniqueBundleIDStr],
                    "message": "Invalid string",
                    "invalid_value": 5,
                },
            ],
        },
        "stage_errors": [],
    }
    assert resp.json["next_stage_structure"] is None


def test_failing_validate_host_path(clients: ClientRegistry) -> None:
    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                configure_components=[
                    FormSpecWrapper(
                        id=FormSpecId("host_data"),
                        form_spec=Dictionary(
                            elements={
                                "host_path": DictElement(
                                    parameter_form=String(
                                        title=Title("Host path"),
                                        field_size=FieldSize.MEDIUM,
                                        custom_validate=(
                                            validators.LengthInRange(min_value=1),
                                            validators.MatchRegex(FOLDER_PATTERN),
                                        ),
                                    ),
                                    required=True,
                                ),
                            }
                        ),
                    ),
                ],
                custom_validators=[_form_spec_extra_validate],
                recap=[],
                button_label="Next",
            ),
        ],
    )
    resp = clients.QuickSetup.send_stage_retrieve_next(
        quick_setup_id="quick_setup_test",
        stages=[{"form_data": {"host_data": {"host_path": "#invalid_host_path#"}}}],
        expect_ok=False,
    )
    resp.assert_status_code(400)
    assert resp.json["errors"] == {
        "formspec_errors": {
            "host_data": [
                {
                    "location": ["host_path"],
                    "message": "Your input does not match the required format '^(?:(?:[~\\\\\\/]|(?:[~\\\\\\/][-_ a-zA-Z0-9.]+)+[~\\\\\\/]?)|[0-9a-fA-F]{32})$'.",
                    "invalid_value": "#invalid_host_path#",
                },
            ],
        },
        "stage_errors": [],
    }
    assert resp.json["next_stage_structure"] is None


def test_quick_setup_save(clients: ClientRegistry) -> None:
    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                configure_components=[
                    widgets.unique_id_formspec_wrapper(Title("account name")),
                ],
                custom_validators=[],
                recap=[],
                button_label="Next",
            ),
        ],
    )
    resp = clients.QuickSetup.complete_quick_setup(
        quick_setup_id="quick_setup_test",
        payload={"button_id": "save", "stages": []},
    )
    resp.assert_status_code(201)
    assert resp.json == {"redirect_url": "http://save/url"}


def test_quick_setup_save_action_exists(clients: ClientRegistry) -> None:
    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                configure_components=[],
                custom_validators=[],
                recap=[],
                button_label="Next",
            ),
        ],
    )
    clients.QuickSetup.complete_quick_setup(
        quick_setup_id="quick_setup_test",
        payload={"button_id": "some_nonexistent_id", "stages": []},
        expect_ok=False,
    ).assert_status_code(404)


def test_unique_id_must_be_unique(
    clients: ClientRegistry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(ConfigBundleStore, "load_for_reading", lambda _: {"I should be unique": {}})

    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                configure_components=[
                    widgets.unique_id_formspec_wrapper(Title("account name")),
                ],
                custom_validators=[qs_validators.validate_unique_id],
                recap=[recaps.recaps_form_spec],
                button_label="Next",
            ),
        ],
    )
    resp = clients.QuickSetup.send_stage_retrieve_next(
        quick_setup_id="quick_setup_test",
        stages=[{"form_data": {UniqueFormSpecIDStr: {UniqueBundleIDStr: "I should be unique"}}}],
        expect_ok=False,
    )
    resp.assert_status_code(400)
    assert len(resp.json["errors"]["stage_errors"]) == 1


def test_get_quick_setup_mode_overview(clients: ClientRegistry) -> None:
    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                sub_title="1",
                configure_components=[
                    widgets.unique_id_formspec_wrapper(Title("account name")),
                ],
                custom_validators=[],
                recap=[],
                button_label="Next",
            ),
            lambda: QuickSetupStage(
                title="stage2",
                sub_title="2",
                configure_components=[],
                custom_validators=[],
                recap=[],
                button_label="Next",
            ),
        ],
    )
    resp = clients.QuickSetup.get_overview_mode_or_guided_mode(
        quick_setup_id="quick_setup_test", mode="overview"
    )
    assert len(resp.json["stages"]) == 2
    assert set(resp.json["stages"][0]) == {"title", "sub_title", "components", "button_label"}


def test_get_quick_setup_overview_prefilled(clients: ClientRegistry) -> None:
    def load_data(obj_id: str) -> ParsedFormData | None:
        return {
            "obj1": {FormSpecId(UniqueFormSpecIDStr): {UniqueBundleIDStr: "foo"}},
            "obj2": {FormSpecId(UniqueFormSpecIDStr): {UniqueBundleIDStr: "bar"}},
        }.get(obj_id)

    register_quick_setup(
        setup_stages=[
            lambda: QuickSetupStage(
                title="stage1",
                sub_title="1",
                configure_components=[
                    widgets.unique_id_formspec_wrapper(Title("account name")),
                ],
                custom_validators=[],
                recap=[],
                button_label="Next",
            ),
        ],
        load_data=load_data,
    )
    resp = clients.QuickSetup.get_overview_mode_or_guided_mode(
        quick_setup_id="quick_setup_test", mode="overview", object_id="obj1"
    )
    assert (
        resp.json["stages"][0]["components"][0]["form_spec"]["spec"]["elements"][0]["default_value"]
        == "foo"
    )

    resp = clients.QuickSetup.get_overview_mode_or_guided_mode(
        quick_setup_id="quick_setup_test", mode="overview", object_id="obj2"
    )
    assert (
        resp.json["stages"][0]["components"][0]["form_spec"]["spec"]["elements"][0]["default_value"]
        == "bar"
    )

    resp = clients.QuickSetup.get_overview_mode_or_guided_mode(
        quick_setup_id="quick_setup_test", mode="overview", object_id="obj3", expect_ok=False
    )
    resp.assert_status_code(404)
