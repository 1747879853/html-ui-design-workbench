const fs = require('fs');
const path = require('path');

const targetFile = path.resolve(__dirname, '../pages/bank-statement-edit.html');
let content = fs.readFileSync(targetFile, 'utf8');

// 1. Cut off everything after </html>
const htmlEndTag = '</html>';
const htmlEndIndex = content.lastIndexOf(htmlEndTag);
if (htmlEndIndex !== -1) {
  content = content.substring(0, htmlEndIndex + htmlEndTag.length) + '\n';
}

// 2. Fix the corrupted block around getCurrencySymbol
const badStart = content.indexOf('// 3.1 所有核销单各原币别金额汇总 (Multi-Currency Settlement Totals)');
const badEnd = content.indexOf('// 资金分段条数据驱动模型 (按单色相区分、悬停联动、点击下钻)');

if (badStart !== -1 && badEnd !== -1) {
  const replacement = `// 3.1 所有核销单各原币别金额汇总 (Multi-Currency Settlement Totals)
        // --------------------------------------------------------------------
        function getCurrencySymbol(curr) {
          if (!curr) return '¥';
          const c = String(curr).toUpperCase();
          if (c === 'USD') return String.fromCharCode(36); // $
          if (c === 'EUR') return '€';
          if (c === 'HKD') return 'HK$';
          if (c === 'GBP') return '£';
          if (c === 'JPY') return 'JP¥';
          return '¥';
        }

        function formatCurrencyAmount(curr, amount) {
          if (amount === null || amount === undefined || isNaN(amount)) return '-';
          const sym = getCurrencySymbol(curr);
          const formattedNum = Number(amount).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
          return sym + formattedNum;
        }

        // 所有核销单合计的各个原币别金额
        const settledOriginalCurrencyTotals = computed(() => {
          const map = {};
          
          settlementList.value.forEach(st => {
            // A. 按费用明细
            if (st.items && Array.isArray(st.items)) {
              st.items.forEach(f => {
                const curr = (f.feeCurrency || currentStatement.currencyCode || 'RMB').toUpperCase();
                const amt = Number(f.settledAmount) || 0;
                map[curr] = (map[curr] || 0) + amt;
              });
            }
            // B. 按发票开出组明细
            if (st.invoiceGroups && Array.isArray(st.invoiceGroups)) {
              st.invoiceGroups.forEach(g => {
                if (g.items && Array.isArray(g.items) && g.items.length > 0) {
                  g.items.forEach(it => {
                    const curr = (it.feeCurrency || g.currencyCode || currentStatement.currencyCode || 'RMB').toUpperCase();
                    const amt = Number(it.settledAmount || it.appliedAmount) || 0;
                    map[curr] = (map[curr] || 0) + amt;
                  });
                } else {
                  const curr = (g.currencyCode || currentStatement.currencyCode || 'RMB').toUpperCase();
                  const amt = Number(g.originalSettledAmount || g.settledAmount || g.totalAmount) || 0;
                  map[curr] = (map[curr] || 0) + amt;
                }
              });
            }
          });

          return Object.entries(map).map(([currency, amount]) => ({
            currency,
            amount: Number(amount.toFixed(2)),
            symbol: getCurrencySymbol(currency),
            formatted: formatCurrencyAmount(currency, amount)
          })).sort((a, b) => b.amount - a.amount);
        });

        // 差值总额 (原始结算折合 - 本次结算合计)
        const totalDiffAmount = computed(() => {
          return settlementList.value.reduce((sum, s) => sum + (Number(s.diffAmount) || 0), 0);
        });

        // 单张核销单的原币别汇总
        function getSettlementOriginalCurrencies(st) {
          const map = {};
          if (st.items && Array.isArray(st.items)) {
            st.items.forEach(f => {
              const curr = (f.feeCurrency || currentStatement.currencyCode || 'RMB').toUpperCase();
              const amt = Number(f.settledAmount) || 0;
              map[curr] = (map[curr] || 0) + amt;
            });
          }
          if (st.invoiceGroups && Array.isArray(st.invoiceGroups)) {
            st.invoiceGroups.forEach(g => {
              if (g.items && Array.isArray(g.items) && g.items.length > 0) {
                g.items.forEach(it => {
                  const curr = (it.feeCurrency || g.currencyCode || currentStatement.currencyCode || 'RMB').toUpperCase();
                  const amt = Number(it.settledAmount || it.appliedAmount) || 0;
                  map[curr] = (map[curr] || 0) + amt;
                });
              } else {
                const curr = (g.currencyCode || currentStatement.currencyCode || 'RMB').toUpperCase();
                const amt = Number(g.originalSettledAmount || g.settledAmount || g.totalAmount) || 0;
                map[curr] = (map[curr] || 0) + amt;
              }
            });
          }
          return Object.entries(map).map(([currency, amount]) => ({
            currency,
            amount: Number(amount.toFixed(2)),
            formatted: formatCurrencyAmount(currency, amount)
          }));
        }

        // 统计关联核销明细与费用总条数
        const totalFeeItemCount = computed(() => {
          let count = 0;
          settlementList.value.forEach(s => {
            if (s.items) count += s.items.length;
            if (s.invoiceGroups) {
              s.invoiceGroups.forEach(g => {
                if (g.items) count += g.items.length;
              });
            }
          });
          return count;
        });

        `;

  content = content.substring(0, badStart) + replacement + content.substring(badEnd);
}

fs.writeFileSync(targetFile, content, 'utf8');
console.log('Fixed syntax and file boundaries cleanly!');
