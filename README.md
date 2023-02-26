# bot_formulaOne

## Description

This script is developed with the finality of develop a telegram bot for get information of [Formula One](https://formula1.com)

## Install all the libraries needed

Install all the libraries needed

```
pip install -r requirements.txt
```

## Configuration config.yaml

Rename file `config.yaml-example` to `config.yaml` and complete the variables with your configuration

```YAML
TELEGRAM:
  TOKEN: TOKEN_TELEGRAM_BOT
  USER_ID: USER_ID

FONE:
  URL_SCHEDULE: https://www.formula1.com/en/racing/2023.html
  URL_COUNTRY: https://www.formula1.com/en/racing/2023/{country}.html
  URL_CIRCUIT: https://www.formula1.com/en/racing/2023/{country}/Circuit.html
  TEXT_INFO_GP: '*{gp_name}* \n\n Date: _{date_gp}_\n Race weekend\n {gp_sessions}'
```


