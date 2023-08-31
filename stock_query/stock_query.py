import pandas as pd
import requests


class StockQuery:
    def __init__(self):
        self.url = "https://www.iwencai.com/gateway/urp/v7/landing/getDataList"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

    def query_stock(self, query: str) -> pd.DataFrame:
        params = {
            "query": query,
            "urp_sort_way": "desc",
            "urp_sort_index": "",
            "page": "1",
            "perpage": "100",
            "addheaderindexes": "",
            "condition": "",
            "codelist": "",
            "indexnamelimit": "",
            "ret": "json_all",
            "source": "Ths_iwencai_Xuangu",
            "urp_use_sort": "1",
            "uuids[0]": "24087",
            "query_type": "stock",
            "comp_id": "6836372",
            "business_cat": "soniu",
            "uuid": "24087",
        }
        response = requests.get(self.url, params=params, headers=self.headers)
        data_json = response.json()
        result_df = pd.DataFrame(data_json["answer"]["components"][0]["data"]["datas"])
        return result_df




if __name__ == "__main__":
    stock_query = StockQuery()
    result = stock_query.query_stock("热度前二十的股票")
    print(result)
