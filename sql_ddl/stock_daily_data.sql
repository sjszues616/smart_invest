create database smart_invest;

CREATE TABLE smart_investment.`a_stock_index_daily_data` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '应用类别ID',
  `date` date NOT NULL DEFAULT '1970-01-01' COMMENT '日期',
  `symbol` varchar(64) NOT NULL DEFAULT '000000' COMMENT '股票代码',
  `open` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '开盘价',
  `close` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '收盘价',
  `high` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '当天最高价',
  `low` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '当天最低价',
  `volume` bigint NOT NULL DEFAULT 0 COMMENT '成交量; 注意单位: 股',
  `amount` decimal(20,2) NOT NULL DEFAULT 0 COMMENT '成交额; 注意单位: 元',
   UNIQUE KEY `unique_date_symbol_q8HeHC9o` (`date`,`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='指数天级数据表';
-- 清空smart_investment 表
delete from smart_investment.a_stock_daily_data;
-- 查看数据
SELECT * FROM smart_investment.a_stock_daily_data  WHERE date > '2024-01-01' and symbol='sh000300'


CREATE TABLE smart_investment.`a_stock_stock_daily_data` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '应用类别ID',
  `date` date NOT NULL DEFAULT '1970-01-01' COMMENT '日期',
  `symbol` varchar(64) NOT NULL DEFAULT '000000' COMMENT '股票代码',
  `open` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '开盘价',
  `close` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '收盘价',
  `high` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '当天最高价',
  `low` decimal(10,2) NOT NULL DEFAULT 0.0 COMMENT '当天最低价',
  `volume` bigint NOT NULL DEFAULT 0 COMMENT '成交量; 注意单位: 股',
  `amount` decimal(20,2) NOT NULL DEFAULT 0 COMMENT '成交额; 注意单位: 元',
  `price_range` decimal(10,2) NOT NULL DEFAULT 0 COMMENT '振幅; 注意单位: %',
  `price_change_percent` decimal(10,2) NOT NULL DEFAULT 0 COMMENT '成交额; 注意单位: %',
  `price_change_amount` decimal(10,2) NOT NULL DEFAULT 0 COMMENT '涨跌额; 注意单位: 元',
  `turnover_rate` decimal(10,2) NOT NULL DEFAULT 0 COMMENT '换手率; 注意单位: %',
   UNIQUE KEY `unique_date_symbol_q8HeHC9o` (`date`,`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='股票天级数据表';