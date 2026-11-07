/**
 * ==============================================================================
 * Ant Design Vue 4.0 UI 优化项目 - 公共逻辑与 Mock 工具库
 * ==============================================================================
 */

// 1. 初始化 Day.js 常用插件
if (window.dayjs) {
  const plugins = [
    'customParseFormat',
    'weekday',
    'localeData',
    'weekOfYear',
    'weekYear',
    'advancedFormat',
    'quarterOfYear'
  ];
  plugins.forEach(p => {
    if (window.dayjs_plugin && window.dayjs_plugin[p]) {
      dayjs.extend(window.dayjs_plugin[p]);
    } else if (window[p]) {
      dayjs.extend(window[p]);
    }
  });
}

// 2. 通用 Mock 数据生成与格式化工具
const MockUtils = {
  // 金额千分位与货币格式化
  formatCurrency(val, currency = '¥', decimals = 2) {
    if (val === null || val === undefined || val === '') return '-';
    const num = Number(val);
    if (isNaN(num)) return '-';
    return `${currency}${num.toLocaleString('zh-CN', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    })}`;
  },

  // 手机号脱敏
  maskPhone(phone) {
    if (!phone) return '-';
    return String(phone).replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
  },

  // 身份证号脱敏
  maskIdCard(id) {
    if (!id) return '-';
    return String(id).replace(/(\d{6})\d{8}(\w{4})/, '$1********$2');
  },

  // 空值安全展示
  safeValue(val, fallback = '-') {
    return (val !== null && val !== undefined && val !== '') ? val : fallback;
  },

  // 生成真实订单模拟数据
  generateOrders(count = 15) {
    const statuses = [
      { code: 'PENDING_PAY', label: '待支付', color: 'warning', badge: 'warning' },
      { code: 'PROCESSING', label: '处理中', color: 'processing', badge: 'processing' },
      { code: 'SHIPPED', label: '已发货', color: 'cyan', badge: 'default' },
      { code: 'COMPLETED', label: '已完成', color: 'success', badge: 'success' },
      { code: 'CANCELLED', label: '已取消', color: 'default', badge: 'error' }
    ];

    const types = ['自营大宗采购', 'B2B 企采直发', '跨境寄售', '保税直邮', '样单采购'];
    const buyers = [
      '北京京东世纪贸易有限公司',
      '深圳市腾讯计算机系统有限公司',
      '阿里巴巴（中国）网络技术有限公司',
      '字节跳动科技有限公司',
      '上海寻梦信息技术有限公司 (拼多多)',
      '美团闪购供应链总部',
      '广州网易计算机系统有限公司',
      '顺丰速运集团华北枢纽中心'
    ];

    const list = [];
    for (let i = 1; i <= count; i++) {
      const statusObj = statuses[i % statuses.length];
      const hasLongText = i % 3 === 0;
      const isEmptyAddress = i === 4;

      list.push({
        id: `ORD-20261018-${String(i).padStart(4, '0')}`,
        index: i,
        orderType: types[i % types.length],
        buyerName: buyers[i % buyers.length],
        buyerContact: `138${Math.floor(10000000 + Math.random() * 90000000)}`,
        status: statusObj.code,
        statusLabel: statusObj.label,
        statusColor: statusObj.color,
        amount: (Math.random() * 85000 + 1200).toFixed(2),
        itemCount: Math.floor(Math.random() * 80) + 1,
        channel: i % 2 === 0 ? '线上商城' : '线下专属合同',
        invoiceStatus: i % 4 === 0 ? '已开票' : (i % 4 === 1 ? '开票中' : '未申请'),
        deliveryAddress: isEmptyAddress 
          ? '' 
          : (hasLongText 
              ? '上海市浦东新区张江高科技园区科苑路88号德国中心三期智能制造大厦B座1804室（进门右拐前台直行第二会议室）' 
              : '北京市海淀区中关村南大街1号科技大厦A座801'),
        remark: hasLongText 
          ? '【客户加急注意】客户要求本批次必须附带原厂检测合格报告（COA与MSDS三份盖章原件），并走顺丰特快冷链运输，若周三前未送达将产生违约金。' 
          : (i % 2 === 0 ? '常规配送，请送货前电话预约。' : ''),
        createdTime: `2026-10-${String((i % 28) + 1).padStart(2, '0')} 14:23:${String((i * 3) % 60).padStart(2, '0')}`,
        updateTime: `2026-10-${String((i % 28) + 1).padStart(2, '0')} 16:45:10`
      });
    }
    return list;
  }
};

// 3. 全局通用主题配置 (遵循 Ant Design Vue 4.0 官方规范，不强行覆盖底层样式)
const GlobalAntdConfig = {
  theme: {
    token: {
      colorPrimary: '#1677ff',
      borderRadius: 6,
      fontSize: 14,
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
      colorBgContainer: '#ffffff',
      colorBgLayout: '#f5f7fa',
      wireframe: false
    },
    components: {
      Card: {
        headerFontSize: 15,
        paddingLG: 20
      },
      Table: {
        headerBg: '#fafafa',
        headerColor: '#1f2329',
        rowHoverBg: '#f0f7ff',
        cellPaddingBlock: 12,
        cellPaddingInline: 12
      },
      Button: {
        controlHeight: 32,
        borderRadius: 4
      }
    }
  }
};

// 导出至全局环境
window.MockUtils = MockUtils;
window.GlobalAntdConfig = GlobalAntdConfig;
