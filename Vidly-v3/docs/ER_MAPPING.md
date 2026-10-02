# ER 映射与新增模型

| ER / 新业务 | Django 实现 |
| --- | --- |
| movies | Movie：可租库存、总库存、条码、售价、上下架 |
| customers | Customer：身份、联系方式、余额、积分 |
| users / roles / operations | Django User / Group / Permission，加服务层角色校验 |
| rent_record / rent_items | Rental / RentalItem：价格快照、租借数量及归还/遗失累计 |
| return_record / return_items | ReturnRecord / ReturnItem：店员验收与每批次结算明细 |
| recharge_items / refund_items | Ledger：余额变动及结余 |
| coupons / customer_coupons | Coupon / CustomerCoupon：每位客户每券限一次 |
| 顾客充值支付 | TopUp：金额、奖励快照、模拟平台流水、状态、退还金额与已回收积分 |
| 积分配置与审计 | RewardPolicy / PolicyRevision |
| 积分流水 | PointsEntry：关联余额流水、增减数和结余 |
| 心愿需求 | MovieWish / WishRequest：一部电影多个顾客、每人一票 |
| 采购与到货 | PurchaseOrder / StockReceipt：采购数量、到货数量、供应商、成本、验收人 |

当前日租金在 Movie，历史日租金在 RentalItem，没有单独费率表；遗失固定五倍，不另建遗失费率表。未实现 ER 中押金，也没有优惠券同种多张数量。

库存：总库存 = 可租库存 + 在外未还数量。采购建单不入库；实物验收同时增加总量与可租量；正常归还只增加可租量；遗失只减少总量。

充值：建单不入账；模拟支付成功后，在一个事务里记录终态、余额、积分、余额流水与积分流水。重复结果不重复发钱/积分。真实支付平台需要另行实现签名验证、服务端回调、对账等。
