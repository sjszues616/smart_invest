create database smart_invest;

CREATE TABLE smart_invest.`a_stock_daily_data` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '应用类别ID',
  `date` date DEFAULT '1970-01-01' COMMENT '日期',
  `open` decimal(10,2) DEFAULT 0.0 COMMENT '开盘价',
  `close` decimal(10,2) DEFAULT 0.0 COMMENT '收盘价',
  `high` decimal(10,2) DEFAULT 0.0 COMMENT '当天最高价',
  `low` decimal(10,2) DEFAULT 0.0 COMMENT '当天最低价',
  `volume` bigint DEFAULT 0 COMMENT '成交量; 注意单位: 股',
  `amount` bigint DEFAULT 0 COMMENT '成交额; 注意单位: 元'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='应用类别定义表';