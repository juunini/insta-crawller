# use guide

### you need chromedriver and selenium(pip3 install selenium)

```
from instaCrawller import *

hashtagUrlCrawller(tag, chromedriverLocation, saveLocation)
userPostUrlCrawller(userID, chromedriverLocation, saveLocation)
postCrawller(urlFile, chromedriverLocation, saveLocation)
followCrawller_instaLogin(urlFile, chromedriverLocation, saveLocation, yourid, yourpassword)
followCrawller_facebookLogin(urlFile, chromedriverLocation, saveLocation, yourid, yourpassword)
```

> `hashtagUrlCrawller(tag, chromedriverLocation, saveLocation)` is<br>
> if you need to crawlling some 'tag', use this. this crawlling post's url.

> `userPostUrlCrawller(userID, chromedriverLocation, saveLocation)` is<br>
> if you need to crawlling some user's post, use this. this crawlling post's url.

> `postCrawller(urlFile, chromedriverLocation, saveLocation)` is<br>
> first, you crawlling post's url, and use this.<br>
> this crawlling post's 'username', 'user url', 'post's updated time', 'hashtags', 'likes', 'image url' to save `delimiter="\t"` csv file.

> `followCrawller_instaLogin(urlFile, chromedriverLocation, saveLocation, yourid, yourpassword)` and<br>
> `followCrawller_facebookLogin(urlFile, chromedriverLocation, saveLocation, yourid, yourpassword)` is<br>
> if you need to SNA you can gathering (follower - user, user - following).

this mechanism is scrolling and crawlling, waiting 6 seconds and repeat.<br>
if you retouch `time.sleep(6)` is less then '6', you meet 'loading failed' again and again and again...
