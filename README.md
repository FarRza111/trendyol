### Trendyol Scraper with FastAPI
Bu layihə FastAPI istifadə edərək Trendyol məhsulları üçün veb skreperdir. Trendyol saytından məhsul məlumatlarını (ad, qiymət, reytinq, və s.) skrap edir, məlumatları SQLite verilənlər bazasında saxlayır və skrap edilmiş məlumatlarla əlaqə yaratmaq üçün RESTful API endpointləri təqdim edir.



### Repository to clone

    git clone git@github.com:FarRza111/trendyol.git
    cd trendyol

### Install packages

    pip install -r requirements.txt

### Run in terminal
    uvicorn main:app --reload


