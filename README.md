#Photo Organizer
##Key Features
- Filter out photos by any EXIF key
- Rename photos with custom format
- Move photos into a organized folder structure

## Image Name Format
|Keyword | Explanation         | Example |
|--------|---------------------|---------|
|YYYY    | Full Year           | 2016    |
|MM      | Month with a 0 when applicable|05|
|DD      | Day with a 0 when applicable|14|
|hh      | Hour with a 0 when applicable|07|
|mm      | Minute with a 0 when applicable|48|
|ss      | Second with a 0 when applicable|44|
|uuu     | Milliseconds with zeros in front when applicable|005|

### Coming Soon
You can insert any EXIF key into the file name with this syntax:
```*|EXIF Keyword|*```

For example: ```YYYY-MM-DD hh.mm.ss.uuu *|Image Model|*```