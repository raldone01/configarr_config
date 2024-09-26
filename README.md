# Sonarr Score Partitioning

Upgrade until: 5000000

The brackets contain the value for the custom formats for Radarr and Sonarr.
The enums are different.

The resolution enum is the same.

* +1000000 Anime Dual Audio
* +2000000 English+German
* +1000000 English only (pick this for english preference)
* +1000000 German only (pick this for german preference)
  Never pick english only and german only at the same time.
* -1000000 Avoid German Mic Dub
* +0210000 Bluray-2160p Remux
* +0200000 Bluray-2160p
* +0190000 Bluray-1080p Remux
* +0180000 Bluray-1080p
* +0170000 WEBDL-2160p
* +0160000 WEBDL-1080p
* +0150000 WebRip-2160p
* +0140000 Bluray-720p
* +0130000 WebRip-1080p
* +0120000 WEBDL-720p
* +0110000 WebRip-720p
* +0100000 Bluray-480p
* +0090000 WEBDL-480p
* +0080000 DVD
* +0070000 WebRip-480p
* +0060000 Raw-HD
* +0050000 HDTV-2160p
* +0040000 HDTV-1080p
* +0030000 HDTV-720p
* +0020000 SDTV-576p (virtual only SDTV exists)
* +0010000 SDTV-480p (virtual only SDTV exists)
* +0000000 Unknown
* +0009999 to 0 Trash guides

# Radarr Score Partitioning

* +2000000 English+German
* +1000000 English only (pick this for english preference)
* +1000000 German only (pick this for german preference)
  Never pick english only and german only at the same time.
* +0260000 Remux-2160p
* +0250000 Bluray-2160p
* +0240000 Remux-1080p
* +0230000 Bluray-1080p
* +0220000 WEBDL-2160p
* +0210000 WEBDL-1080p
* +0200000 WebRip-2160p
* +0190000 Bluray-720p
* +0180000 WebRip-1080p
* +0170000 Bluray-576p
* +0160000 WEBDL-720p
* +0150000 WebRip-720p
* +0140000 Bluray-480p
* +0130000 WEBDL-480p
* +0120000 DVD
* +0110000 WebRip-480p
* +0100000 DVD-R
* +0090000 Raw-HD
* +0080000 HDTV-2160p
* +0070000 HDTV-1080p
* +0060000 HDTV-720p
* +0050000 SDTV-576p (virtual only SDTV exists)
* +0040000 SDTV-480p (virtual only SDTV exists)
* +0030000 TELECINE
* +0020000 TELESYNC
* +0010000 CAM
* +0000000 Unknown
* -0010000 DVDSCR
* -0010000 REGIONAL
* -0010000 BR-DISK
* -0010000 WORKPRINT
* +0009999 to 0 Trash guides

# Condition names:

| Radarr           | Sonarr     |
| ---------------- | ---------- |
| Source           | Source     |
| Resolution       | Resolution |
| Quality Modifier |            |

# Resolution enum:

* 0: Unknown
* 360: 360p
* 480: 480p
* 540: 540p
* 576: 576p
* 720: 720p
* 1080: 1080p
* 2160: 2160p
