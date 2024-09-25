from enum import Enum
import os
import logging
import json

score_multiplier = 10000


class RadarrSourceEnum(Enum):
    UNKNOWN = 0
    CAM = 1
    TELESYNC = 2
    TELECINE = 3
    WORKPRINT = 4
    DVD = 5
    TELEVISION = 6
    WEBDL = 7
    WEBRIP = 8
    BLURAY = 9


class RadarrModifierEnum(Enum):
    NONE = 0
    REGIONAL = 1
    SCREENER = 2
    RAWHD = 3
    BRDISK = 4
    REMUX = 5


class SonarrSourceEnum(Enum):
    UNKNOWN = 0
    TELEVISION = 1
    TELEVISION_RAW = 2
    WEBDL = 3
    WEBRIP = 4
    DVD = 5
    BLURAY = 6
    BLURAY_RAW = 7  # Remux


# https://github.com/Sonarr/Sonarr/blob/develop/src/NzbDrone.Core/Qualities/Quality.cs
sonarr_source_classes_to_generate = [
    {
        "source_class": SonarrSourceEnum.BLURAY_RAW,
        "full_class_name": "bluray-2160p-remux",
        "full_class_name_pretty": "Bluray-2160p Remux",
        "resolution": 2160,
        "custom_format_score": 20,
    },
    {
        "source_class": SonarrSourceEnum.BLURAY,
        "full_class_name": "bluray-2160p",
        "full_class_name_pretty": "Bluray-2160p",
        "resolution": 2160,
        "custom_format_score": 19,
    },
    {
        "source_class": SonarrSourceEnum.BLURAY_RAW,
        "full_class_name": "bluray-1080p-remux",
        "full_class_name_pretty": "Bluray-1080p Remux",
        "resolution": 1080,
        "custom_format_score": 18,
    },
    {
        "source_class": SonarrSourceEnum.BLURAY,
        "full_class_name": "bluray-1080p",
        "full_class_name_pretty": "Bluray-1080p",
        "resolution": 1080,
        "custom_format_score": 17,
    },
    {
        "source_class": SonarrSourceEnum.WEBDL,
        "full_class_name": "webdl-2160p",
        "full_class_name_pretty": "WEBDL-2160p",
        "resolution": 2160,
        "custom_format_score": 16,
    },
    {
        "source_class": SonarrSourceEnum.WEBDL,
        "full_class_name": "webdl-1080p",
        "full_class_name_pretty": "WEBDL-1080p",
        "resolution": 1080,
        "custom_format_score": 15,
    },
    {
        "source_class": SonarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-2160p",
        "full_class_name_pretty": "WEBRip-2160p",
        "resolution": 2160,
        "custom_format_score": 14,
    },
    {
        "source_class": SonarrSourceEnum.BLURAY,
        "full_class_name": "bluray-720p",
        "full_class_name_pretty": "Bluray-720p",
        "resolution": 720,
        "custom_format_score": 13,
    },
    {
        "source_class": SonarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-1080p",
        "full_class_name_pretty": "WEBRip-1080p",
        "resolution": 1080,
        "custom_format_score": 12,
    },
    {
        "source_class": SonarrSourceEnum.WEBDL,
        "full_class_name": "webdl-720p",
        "full_class_name_pretty": "WEBDL-720p",
        "resolution": 720,
        "custom_format_score": 11,
    },
    {
        "source_class": SonarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-720p",
        "full_class_name_pretty": "WEBRip-720p",
        "resolution": 720,
        "custom_format_score": 10,
    },
    {
        "source_class": SonarrSourceEnum.BLURAY,
        "full_class_name": "bluray-480p",
        "full_class_name_pretty": "Bluray-480p",
        "resolution": 480,
        "custom_format_score": 9,
    },
    {
        "source_class": SonarrSourceEnum.WEBDL,
        "full_class_name": "webdl-480p",
        "full_class_name_pretty": "WEBDL-480p",
        "resolution": 480,
        "custom_format_score": 8,
    },
    {
        "source_class": SonarrSourceEnum.DVD,
        "full_class_name": "dvd",
        "full_class_name_pretty": "DVD",
        "custom_format_score": 7,
    },
    {
        "source_class": SonarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-480p",
        "full_class_name_pretty": "WEBRip-480p",
        "resolution": 480,
        "custom_format_score": 6,
    },
    {
        "source_class": SonarrSourceEnum.TELEVISION_RAW,
        "full_class_name": "raw-hd",
        "full_class_name_pretty": "Raw-HD",
        "resolution": 2160,
        "custom_format_score": 5,
    },
    {
        "source_class": SonarrSourceEnum.TELEVISION,
        "full_class_name": "hdtv-2160p",
        "full_class_name_pretty": "HDTV-2160p",
        "resolution": 2160,
        "custom_format_score": 4,
    },
    {
        "source_class": SonarrSourceEnum.TELEVISION,
        "full_class_name": "hdtv-1080p",
        "full_class_name_pretty": "HDTV-1080p",
        "resolution": 1080,
        "custom_format_score": 3,
    },
    {
        "source_class": SonarrSourceEnum.TELEVISION,
        "full_class_name": "hdtv-720p",
        "full_class_name_pretty": "HDTV-720p",
        "resolution": 720,
        "custom_format_score": 2,
    },
    {
        "source_class": SonarrSourceEnum.TELEVISION,
        "full_class_name": "sdtv-576p",
        "full_class_name_pretty": "SDTV-576p",
        "resolution": 576,
        "custom_format_score": 1,
    },
    {
        "source_class": SonarrSourceEnum.TELEVISION,
        "full_class_name": "sdtv-480p",
        "full_class_name_pretty": "SDTV-480p",
        "resolution": 480,
        "custom_format_score": 1,
    },
    {
        "source_class": SonarrSourceEnum.UNKNOWN,
        "full_class_name": "unknown",
        "full_class_name_pretty": "Unknown",
        "custom_format_score": 0,
    },
]

# https://github.com/Radarr/Radarr/blob/be2e1e4fdb08ead3424ee24b191c988241a8b7b6/src/NzbDrone.Core/Qualities/Quality.cs#L93
radarr_source_classes_to_generate = [
    {
        "source_class": RadarrSourceEnum.BLURAY,
        "full_class_name": "bluray-2160p-remux",
        "full_class_name_pretty": "Remux-2160p",
        "resolution": 2160,
        "modifier_is": RadarrModifierEnum.REMUX,
        "custom_format_score": 26,
    },
    {
        "source_class": RadarrSourceEnum.BLURAY,
        "full_class_name": "bluray-2160p",
        "full_class_name_pretty": "Bluray-2160p",
        "resolution": 2160,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 25,
    },
    {
        "source_class": RadarrSourceEnum.BLURAY,
        "full_class_name": "bluray-1080p-remux",
        "full_class_name_pretty": "Remux-1080p",
        "resolution": 1080,
        "modifier_is": RadarrModifierEnum.REMUX,
        "custom_format_score": 24,
    },
    {
        "source_class": RadarrSourceEnum.BLURAY,
        "full_class_name": "bluray-1080p",
        "full_class_name_pretty": "Bluray-1080p",
        "resolution": 1080,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 23,
    },
    {
        "source_class": RadarrSourceEnum.WEBDL,
        "full_class_name": "webdl-2160p",
        "full_class_name_pretty": "WEBDL-2160p",
        "resolution": 2160,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 22,
    },
    {
        "source_class": RadarrSourceEnum.WEBDL,
        "full_class_name": "webdl-1080p",
        "full_class_name_pretty": "WEBDL-1080p",
        "resolution": 1080,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 21,
    },
    {
        "source_class": RadarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-2160p",
        "full_class_name_pretty": "WEBRip-2160p",
        "resolution": 2160,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 20,
    },
    {
        "source_class": RadarrSourceEnum.BLURAY,
        "full_class_name": "bluray-720p",
        "full_class_name_pretty": "Bluray-720p",
        "resolution": 720,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 19,
    },
    {
        "source_class": RadarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-1080p",
        "full_class_name_pretty": "WEBRip-1080p",
        "resolution": 1080,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 18,
    },
    {
        "source_class": RadarrSourceEnum.WEBDL,
        "full_class_name": "bluray-576p",
        "full_class_name_pretty": "Bluray-576p",
        "resolution": 576,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 17,
    },
    {
        "source_class": RadarrSourceEnum.WEBDL,
        "full_class_name": "webdl-720p",
        "full_class_name_pretty": "WEBDL-720p",
        "resolution": 720,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 16,
    },
    {
        "source_class": RadarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-720p",
        "full_class_name_pretty": "WEBRip-720p",
        "resolution": 720,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 15,
    },
    {
        "source_class": RadarrSourceEnum.BLURAY,
        "full_class_name": "bluray-480p",
        "full_class_name_pretty": "Bluray-480p",
        "resolution": 480,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 14,
    },
    {
        "source_class": RadarrSourceEnum.WEBDL,
        "full_class_name": "webdl-480p",
        "full_class_name_pretty": "WEBDL-480p",
        "resolution": 480,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 13,
    },
    {
        "source_class": RadarrSourceEnum.DVD,
        "full_class_name": "dvd",
        "full_class_name_pretty": "DVD",
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 12,
    },
    {
        "source_class": RadarrSourceEnum.WEBRIP,
        "full_class_name": "webrip-480p",
        "full_class_name_pretty": "WEBRip-480p",
        "resolution": 480,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 11,
    },
    {
        "source_class": RadarrSourceEnum.DVD,
        "full_class_name": "dvd-r",
        "full_class_name_pretty": "DVD-R",
        "resolution": 480,
        "modifier_is": RadarrModifierEnum.REMUX,
        "custom_format_score": 10,
    },
    {
        "source_class": RadarrSourceEnum.TELEVISION,
        "full_class_name": "raw-hd",
        "full_class_name_pretty": "Raw-HD",
        "resolution": 1080,
        "modifier_is": RadarrModifierEnum.RAWHD,
        "custom_format_score": 9,
    },
    {
        "source_class": RadarrSourceEnum.TELEVISION,
        "full_class_name": "hdtv-2160p",
        "full_class_name_pretty": "HDTV-2160p",
        "resolution": 2160,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 8,
    },
    {
        "source_class": RadarrSourceEnum.TELEVISION,
        "full_class_name": "hdtv-1080p",
        "full_class_name_pretty": "HDTV-1080p",
        "resolution": 1080,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 7,
    },
    {
        "source_class": RadarrSourceEnum.TELEVISION,
        "full_class_name": "hdtv-720p",
        "full_class_name_pretty": "HDTV-720p",
        "resolution": 720,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 6,
    },
    {
        "source_class": RadarrSourceEnum.TELEVISION,
        "full_class_name": "sdtv-576p",
        "full_class_name_pretty": "SDTV-576p",
        "resolution": 576,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 5,
    },
    {
        "source_class": RadarrSourceEnum.TELEVISION,
        "full_class_name": "sdtv-480p",
        "full_class_name_pretty": "SDTV-480p",
        "resolution": 480,
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 4,
    },
    {
        "source_class": RadarrSourceEnum.TELECINE,
        "full_class_name": "telecine",
        "full_class_name_pretty": "TELECINE",
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 3,
    },
    {
        "source_class": RadarrSourceEnum.TELESYNC,
        "full_class_name": "telesync",
        "full_class_name_pretty": "TELESYNC",
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 2,
    },
    {
        "source_class": RadarrSourceEnum.CAM,
        "full_class_name": "cam",
        "full_class_name_pretty": "CAM",
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": 1,
    },
    {
        "source_class": RadarrSourceEnum.UNKNOWN,
        "full_class_name": "unknown",
        "full_class_name_pretty": "Unknown",
        "custom_format_score": 0,
    },
    {
        "source_class": RadarrSourceEnum.DVD,
        "full_class_name": "dvdscr",
        "full_class_name_pretty": "DVDSCR",
        "resolution": 480,
        "modifier_is": RadarrModifierEnum.SCREENER,
        "custom_format_score": -1,
    },
    {
        "source_class": RadarrSourceEnum.DVD,
        "full_class_name": "regional",
        "full_class_name_pretty": "REGIONAL",
        "resolution": 480,
        "modifier_is": RadarrModifierEnum.REGIONAL,
        "custom_format_score": -1,
    },
    {
        "source_class": RadarrSourceEnum.BLURAY,
        "full_class_name": "br-disk",
        "full_class_name_pretty": "BR-DISK",
        "resolution": 1080,
        "modifier_is": RadarrModifierEnum.BRDISK,
        "custom_format_score": -1,
    },
    {
        "source_class": RadarrSourceEnum.WORKPRINT,
        "full_class_name": "workprint",
        "full_class_name_pretty": "WORKPRINT",
        "modifier_is": RadarrModifierEnum.NONE,
        "custom_format_score": -1,
    },
]

format_resolution_specification = """
,
{{
  "name": "{resolution}p",
  "implementation": "ResolutionSpecification",
  "negate": false,
  "required": true,
  "fields": {{ "value": {resolution} }}
}}
"""

format_radarr_is_modifier = """
,
{{
  "name": "{modifier_name}",
  "implementation": "QualityModifierSpecification",
  "negate": false,
  "required": true,
  "fields": {{ "value": {modifier_enum_value} }}
}}
"""

format_custom_format_score = """
{{
  "trash_id": "custom-{arr_type_lower}-source-class-{full_class_name}",
  "trash_scores": {{
    "default": {custom_format_score}
  }},
  "trash_description": "Matches releases that are {full_class_name_pretty}. {arr_type} only.",
  "name": "Source class: {full_class_name_pretty}",
  "includeCustomFormatWhenRenaming": false,
  "specifications":
    [
      {{
        "name": "{full_class_name_pretty}",
        "implementation": "SourceSpecification",
        "negate": false,
        "required": true,
        "fields": {{ "value": {class_enum_value} }}
      }}
      {formatted_resolution_specification}
      {formatted_is_modifier}
    ]
}}
"""

format_naming_scheme = "_{arr_type_lower}_source_class_{class_name}"

if __name__ == "__main__":
    # Change working directory to the script's directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Generate Sonarr source classes
    for source_class in sonarr_source_classes_to_generate:
        logging.info(
            f"Generating Sonarr source class: {source_class['full_class_name']}"
        )
        full_class_name = source_class["full_class_name"]
        full_class_name_pretty = source_class["full_class_name_pretty"]
        resolution = source_class.get("resolution")
        custom_format_score = source_class["custom_format_score"]
        source_class_enum = source_class["source_class"].name

        # if unknown skip
        if source_class_enum == SonarrSourceEnum.UNKNOWN.name:
            continue

        class_enum_value = source_class["source_class"].value
        arr_type = "Sonarr"
        arr_type_lower = arr_type.lower()

        formatted_resolution_specification = ""
        if resolution:
            formatted_resolution_specification = format_resolution_specification.format(
                resolution=resolution
            )

        formatted_custom_format_score = format_custom_format_score.format(
            full_class_name=full_class_name,
            full_class_name_pretty=full_class_name_pretty,
            custom_format_score=custom_format_score * score_multiplier,
            class_enum_value=class_enum_value,
            arr_type=arr_type,
            arr_type_lower=arr_type_lower,
            formatted_resolution_specification=formatted_resolution_specification,
            formatted_is_modifier="",
        )
        formatted_naming_scheme = format_naming_scheme.format(
            class_name=full_class_name, arr_type_lower=arr_type_lower
        )
        # Parse and then pretty print the JSON
        parsed_json = json.loads(formatted_custom_format_score)
        formatted_custom_format_score = json.dumps(parsed_json, indent=2)
        # Append a newline to the end of the JSON
        formatted_custom_format_score += "\n"
        with open(f"cfs/{formatted_naming_scheme}.json", "w") as f:
            f.write(formatted_custom_format_score)

    # Generate Radarr source classes
    for source_class in radarr_source_classes_to_generate:
        logging.info(
            f"Generating Radarr source class: {source_class['full_class_name']}"
        )
        full_class_name = source_class["full_class_name"]
        full_class_name_pretty
        resolution = source_class.get("resolution")
        custom_format_score = source_class["custom_format_score"]
        source_class_enum = source_class["source_class"].name

        # if unknown skip
        if source_class_enum == RadarrSourceEnum.UNKNOWN.name:
            continue

        class_enum_value = source_class["source_class"].value
        arr_type = "Radarr"
        arr_type_lower = arr_type.lower()
        modifier_is = source_class.get("modifier_is")
        modifier_name = modifier_is.name if modifier_is else None
        modifier_enum_value = modifier_is.value if modifier_is else None

        formatted_resolution_specification = ""
        if resolution:
            formatted_resolution_specification = format_resolution_specification.format(
                resolution=resolution
            )

        formatted_is_modifier = ""
        if modifier_is:
            formatted_is_modifier = format_radarr_is_modifier.format(
                modifier_name=modifier_name, modifier_enum_value=modifier_enum_value
            )

        formatted_custom_format_score = format_custom_format_score.format(
            full_class_name=full_class_name,
            full_class_name_pretty=full_class_name_pretty,
            custom_format_score=custom_format_score * score_multiplier,
            class_enum_value=class_enum_value,
            arr_type=arr_type,
            arr_type_lower=arr_type_lower,
            formatted_resolution_specification=formatted_resolution_specification,
            formatted_is_modifier=formatted_is_modifier,
        )
        formatted_naming_scheme = format_naming_scheme.format(
            class_name=full_class_name, arr_type_lower=arr_type_lower
        )
        # Parse and then pretty print the JSON
        parsed_json = json.loads(formatted_custom_format_score)
        formatted_custom_format_score = json.dumps(parsed_json, indent=2)
        # Append a newline to the end of the JSON
        formatted_custom_format_score += "\n"
        with open(f"cfs/{formatted_naming_scheme}.json", "w") as f:
            f.write(formatted_custom_format_score)
