# Sounimei
[搜你妹](https://wsmusic.sounm.com/)Lossless music download

## Feature
- Automatic analysis of [QR code](https://wsmusic.sounm.com/unlock) for unlocking
- Enter keywords and download in batch

## How to use
- Create database "music"
  > CREATE DATABASE `music`
- Environment: Python 3.8
- Need [JAVA](https://www.java.com/zh_CN/download/mac_download.jsp) to read QR, you can read this QR by your camera, too
- Run
  > python3 scraper.py
- If you use [docker](https://www.docker.com/)
  > docker pull tunogya/chrome:v1.0
- git clone
  > git clone https://github.com/tunogya/Sounimei.git

## Database
| Name       | Type    | Length | Not Null | Key | Comment      |
|------------|---------|--------|----------|-----|--------------|
| id         | int     | 11     | Y        | Y   |              |
| file\_name | varchar | 24     | Y        |     | Unique index |
| titlle     | varchar | 255    | Y        |     | index        |
| singer     | varchar | 255    | Y        |     | index        |
| album      | varchar | 255    | Y        |     | index        |
| url        | varchar | 255    | Y        |     |              |

## Disclaimer
This software is only for study.
If you download pirated content or have other business activities, you are responsible for it.
