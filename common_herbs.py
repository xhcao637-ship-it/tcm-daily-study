# 常用中药材清单 — 按功效分类
# P0 = 临床最常用（教材必学）
# 来源：中医药大学本科教材《中药学》+ 《中国药典》高频药材

COMMON_HERBS = {
    # === 解表药 ===
    "mahuang": 0, "guizhi": 0, "zisuye": 0, "jingjie": 0, "fangfeng": 0,
    "qianghuo": 0, "baizhi": 0, "xiangru": 0, "shengjiang": 0, "congbai": 0,
    "xinyi": 0, "cangerzi": 0, "bohe": 0, "niubangzi": 0, "sangye": 0,
    "juhua": 0, "chaihu": 0, "gegen": 0, "shengma": 0, "manjingzi": 0,
    "dandouchi": 0, "muge": 0,
    # === 清热药 ===
    "shigao": 0, "zhimu": 0, "zhizi": 0, "xiakucao": 0, "lugen": 0,
    "tianzhuhuang": 0, "juemingzi": 0, "gujingcao": 0,
    "huangqin": 0, "huanglian": 0, "huangbai": 0, "longdancao": 0,
    "kucanshen": 0, "baitouwen": 0,
    "jinyinhua": 0, "lianqiao": 0, "pugongying": 0, "zihuadiding": 0,
    "yuxingcao": 0, "banlangen": 0, "shegan": 0, "shanyinhua": 0,
    "chuanxinlian": 0, "baijiangcao": 0, "baituling": 0,
    "shengdihuang": 0, "xuanshen": 0, "mudanpi": 0, "chishao": 0,
    "zicao": 0, "shuiniujiao": 0,
    "qinghao": 0, "digupi": 0, "baiwei": 0, "yinchaihu": 0, "huhuanglian": 0,
    # === 泻下药 ===
    "dahuang": 0, "mangxiao": 0, "luhui": 0, "fanxieye": 0,
    "huomaren": 0, "yuliren": 0,
    # === 祛风湿药 ===
    "duhuo": 0, "weiling": 0, "fangji": 0, "qinjiao": 0,
    "sangzhi": 0, "haifengteng": 0, "chuanwu": 0,
    "wujiapi": 0, "sangjisheng": 0, "gouji": 0, "qiannianjian": 0,
    # === 化湿药 ===
    "huoxiang": 0, "peilan": 0, "cangzhu": 0, "houpo": 0,
    "sharen": 0, "baidoukou": 0, "caodoukou": 0,
    # === 利水渗湿药 ===
    "fuling": 0, "zhuling": 0, "yiyiren": 0, "zexie": 0,
    "cheqianzi": 0, "huashi": 0, "mutong": 0, "tongcao": 0,
    "qumai": 0, "bianxu": 0, "difu": 0, "dongguapi": 0,
    "yinchenhao": 0, "jinqiancao": 0, "haijiinsha": 0,
    "bijiezi": 0,
    # === 温里药 ===
    "fuzi": 0, "ganjiang": 0, "rougui": 0, "wuzhuyu": 0,
    "xiaohuixiang": 0, "dingxiang": 0, "gaoliangjiang": 0,
    "huajiao": 0, "biba": 0,
    # === 理气药 ===
    "chenpi": 0, "qingpi": 0, "zhishi": 0, "zhiqiao": 0,
    "muxiang": 0, "xiangfu": 0, "wuyao": 0, "tanxiang": 0,
    "chenxiang": 0, "chuanlianzi": 0, "litchi": 0, "foshou": 0,
    "meiguihua": 0, "xiangchun": 0,
    # === 消食药 ===
    "shanzha": 0, "shenqu": 0, "maiya": 0, "guya": 0,
    "laifuzi": 0, "jineijin": 0,
    # === 止血药 ===
    "xiaoji": 0, "daji": 0, "diyu": 0, "huaihua": 0,
    "cebaiye": 0, "baimaogen": 0, "sanqi": 0, "qiancaogen": 0,
    "puhuang": 0, "aiye": 0, "baiji": 0, "xianhecao": 0,
    # === 活血化瘀药 ===
    "chuanxiong": 0, "yanhusuo": 0, "yujin": 0, "jianghuang": 0,
    "ruxiang": 0, "moyao": 0, "wulingzhi": 0, "danshen": 0,
    "honghua": 0, "taoren": 0, "yimucao": 0, "niuxi": 0,
    "jixueteng": 0, "wangjiangliu": 0, "tubiechong": 0,
    "xuejie": 0, "zelan": 0, "sanleng": 0, "ezhu": 0,
    # === 化痰止咳平喘药 ===
    "banxia": 0, "tiannanxing": 0, "baifuzi": 0, "baijiezi": 0,
    "xuanfuhua": 0, "chuanbeimu": 0, "zhebeimu": 0, "gualou": 0,
    "zhuru": 0, "kunbu": 0, "haizao": 0, "huangyangjie": 0,
    "jiegeng": 0, "xingren": 0, "ziwan": 0, "kuandonghua": 0,
    "pipaye": 0, "sangbaipi": 0, "tinglizi": 0, "baixianpi": 0,
    # === 安神药 ===
    "suanzaoren": 0, "baiziren": 0, "yuanzhi": 0, "hehuanpi": 0,
    "yejiaoteng": 0, "longgu": 0, "muli": 0, "zhensha": 0,
    "cishi": 0, "hupo": 0,
    # === 平肝息风药 ===
    "shijueming": 0, "mudili": 0, "daizheshi": 0, "lingyangjiaofen": 0,
    "gouteng": 0, "tianma": 0, "dilong": 0, "quanxie": 0,
    "wugong": 0, "jiangcan": 0,
    # === 开窍药 ===
    "shexiang": 0, "bingpian": 0, "shichangpu": 0, "suhexiang": 0,
    # === 补气药 ===
    "renshen": 0, "xiyangshen": 0, "dangshen": 0, "taizishen": 0,
    "huangqi": 0, "baizhu": 0, "shanyao": 0, "gancao": 0,
    "dazao": 0, "fengmi": 0, "baibiandou": 0,
    # === 补血药 ===
    "dangui": 0, "shudi": 0, "baishaoyao": 0, "heshouwu": 0,
    "ejiao": 0, "longyanrou": 0,
    # === 补阴药 ===
    "beishashen": 0, "nanshashen": 0, "maidong": 0, "tianmendong": 0,
    "shihu": 0, "yuzhu": 0, "huangjing": 0, "gouqizi": 0,
    "nvzhenzi": 0, "mohanlian": 0, "guiban": 0, "biejia": 0,
    # === 补阳药 ===
    "lurong": 0, "bajitian": 0, "yinyanghuo": 0, "duzhong": 0,
    "xuduan": 0, "gouji": 0, "buguzhi": 0, "yizhiren": 0,
    "tusizi": 0, "shayuanzi": 0, "dongchongxiacao": 0,
    "gejiezi": 0, "hetaorou": 0, "ziheche": 0,
    # === 收涩药 ===
    "wuweizi": 0, "wumei": 0, "wubeizi": 0, "roudoukou": 0,
    "chishizhi": 0, "hezi": 0, "shanzhuyou": 0, "sangpiaoxiao": 0,
    "fupenzi": 0, "jinyingzi": 0, "lianzi": 0, "qianshi": 0,
}
