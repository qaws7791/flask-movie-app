## Start Code

pip install flask pymongo python-dotenv

## Site Map

|                            |                                        |      |
| -------------------------- | -------------------------------------- | ---- |
| /                          | 메인 페이지                            |      |
| /movie/[id]                | 코멘트 페이지                          |      |
| /api/comment/?movieid=[id] | 코멘트 생성, 특정 영화 코멘트 가져오기 |      |
| /api/recent/[limit]        | 최근 코멘트 가져오기                   |      |
| /api/genre/[genre]         | 특정 장르 코멘트 가져오기              |      |



## API

| api            | page                                                      |
| -------------- | --------------------------------------------------------- |
| 영화 검색      | https://developers.themoviedb.org/3/search/search-movies  |
| 영화 장르 목록 | https://developers.themoviedb.org/3/genres/get-movie-list |
