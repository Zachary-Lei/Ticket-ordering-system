# Ticket-ordering-system
Django+python+MySQL

      机票在线预订系统项目使用python + MySQL + Django开发，实现用户在线查询航班信息、
  预订机票、查看订单、支付订单、取消订单等功能
      数据库设计使用MySQL，ER图尽量设计严谨，比如user与person的关系是有两种，一种是
  实名注册时，一个person可以有多个user，一种是一个user购买机票可以指定多个person，因
  此引入两种联系集；同时为了能够实现自动更新保持一致性，设计支付订单、取消订单等功能对应
  的触发器；为了更好显示页面数据，定义相关视图；保证表中的相关属性遵守完整性约束；综合上，
  数据库设计较为严谨。
      为了保证前端显示效果，使用Bootstrap开发框架，提供了优雅的HTML和CSS规范。
