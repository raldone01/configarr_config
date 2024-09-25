# Radarr/Sonarr Score Partitioning with source classes

Upgrade until: 5000000

The brackets contain the value for the custom formats for Radarr and Sonarr.
The enums are different.

The resolution enum is the same.

# Radarr/Sonarr Score Partitioning Legacy

Upgrade until: 5000000

The brackets contain the value for the custom formats for Radarr and Sonarr.
The enums are different.

The resolution enum is the same.

* +0009999 to 0 Trash guides
* +0020000 REMUX (r5)
  The REMUX modifier is worth two resolution steps.
* +0010000 360p (360)
* +0020000 480p (480)
* +0030000 540p (540)
* +0040000 576p (576)
* +0050000 720p (720)
* +0060000 1080p (1080)
* +0070000 2160p (2160)
* +0000000 UNKNOWN (r0)
* +0100000 CAM (r1)
* +0200000 TELESYNC (r2)
* +0300000 TELECINE (r3)
* +0000000 WORKPRINT (r4)
* +0400000 TV (r6)
* +0500000 DVD (r5)
* +0600000 WEBRIP (r8)
* +0700000 WEBDL (r7)
* +0800000 Bluray (r9)
* +0000000 UNKNOWN (s0)
* +0100000 Television (s1)
* +0000000 TelevisionRaw (s2)
* +0200000 DVD (s5)
* +0300000 WEBRIP (s4)
* +0400000 WEBDL (s3)
* +0500000 Bluray (s6)
* +0600000 BlurayRaw (s7) (This is the remux for shows)
* -1000000 Avoid German Mic Dub
* +1000000 English only (pick this for english preference)
* +1000000 German only (pick this for german preference)
* +2000000 English+German

Never pick english only and german only at the same time.

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
