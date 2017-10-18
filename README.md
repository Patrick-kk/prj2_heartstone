# prj2_heartstone
项目二： 

先用爬虫把炉石的卡牌图片全爬出来并下载，然后通过图像识别卡中的文字，再结合https://api.hearthstonejson.com/v1/ 这里给的数据整理成我们自己的卡牌库，支持搜索和分类 

第一部分 
1. 先到 hs.blizzard.cn/cards/，把卡牌图片都抓下来，（需要按职业进行区分，为第二部分做准备） 
2. 利用PIL对图片进行截取，把卡牌名字/卡牌描述截取下来（可以关注一下opencv） 
3. 因卡牌名字有些是进行了形变，可能需要处理一下才能提高识别率 
4. 利用tesseract进行文字识别  

第二部分暂时没理解怎么整理自己的卡牌库


Update(2017-10-19, kk)
通过 http://hs.blizzard.cn/action/cards/query 可以获取完整卡牌信息的JSON，图片识别就非必要了
