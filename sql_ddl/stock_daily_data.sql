CREATE TABLE test.`smart_invest` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '应用类别ID',
  `date` datetime(10) DEFAULT '1970-01-01' COMMENT '日期',
  `open` decimal(10,2) DEFAULT 0.0 COMMENT '开盘价',
  `close` decimal(10,2) DEFAULT 0.0 COMMENT '收盘价',
  `high` decimal(10,2) DEFAULT 0.0 COMMENT '当天最高价',
  `low` decimal(10,2) DEFAULT 0.0 COMMENT '当天最低价',
  `volume` bigint DEFAULT 0 COMMENT '成交量; 注意单位: 股',
  `amount` bigint DEFAULT 0 COMMENT '成交额; 注意单位: 元'
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=233 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='应用类别定义表';