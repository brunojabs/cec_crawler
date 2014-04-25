CEC Crawler
===========

Crawler de busca do site CEC.
Mini crawler para extrair informações da página de busca do site CEC


Como usar
--------

    pip install -r requirements.txt
    python crawler.py <parametro de busca>


Exemplo:
--------

    python crawler.py tijolo


Estrutura DB:
--------

```plaintext
# Products
+-----------------------------------+-------+---------+----------------------------------+----------------------------+
|               name                | price |  brand  |             img_url              |            url             |
+-----------------------------------+-------+---------+----------------------------------+----------------------------+
| Tijolo Refratário 11,5x23x5,1cm - |  5.8  | Martins | http://www.cec.com.br/image_path | http://www.cec.com.br/prod |
+-----------------------------------+-------+---------+----------------------------------+----------------------------+
```
