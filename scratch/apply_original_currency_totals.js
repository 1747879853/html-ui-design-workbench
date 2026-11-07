const fs = require('fs');
const path = require('path');

const targetFile = path.resolve(__dirname, '../pages/bank-statement-edit.html');
let content = fs.readFileSync(targetFile, 'utf8');

// 1. Add CSS styles for multi-currency summary
const cssMarker = '.expanded-detail-box {';
const newCss = `
    /* 所有核销单原币合计看板横幅与胶囊 */
    .settlement-currency-summary-bar {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 6px 12px;
      margin: 10px 14px 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }

    .summary-bar-left {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .summary-bar-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 12px;
      font-weight: 700;
      color: #334155;
    }

    .summary-currency-pills {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    .summary-curr-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 1px 8px;
      border-radius: 4px;
      font-size: 12px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .summary-curr-tag.tag-curr-usd {
      border-color: #bfdbfe;
      background: #eff6ff;
      color: #1e40af;
    }

    .summary-curr-tag.tag-curr-rmb,
    .summary-curr-tag.tag-curr-cny {
      border-color: #fed7aa;
      background: #fff7ed;
      color: #9a3412;
    }

    .summary-curr-tag.tag-curr-eur {
      border-color: #e9d5ff;
      background: #faf5ff;
      color: #6b21a8;
    }

    .summary-curr-tag.tag-curr-hkd {
      border-color: #fde68a;
      background: #fffbeb;
      color: #854d0e;
    }

    .curr-symbol-badge {
      font-size: 10px;
      font-weight: 800;
      padding: 0 4px;
      border-radius: 3px;
      background: rgba(0, 0, 0, 0.06);
    }

    .curr-amount-val {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-weight: 700;
      font-variant-numeric: tabular-nums;
    }

    .summary-bar-right {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 11.5px;
      color: #64748b;
      margin-left: auto;
    }

    .summary-meta-item {
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .summary-meta-sep {
      color: #cbd5e1;
    }

    .meta-val {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: #1e293b;
      font-weight: 600;
    }

    .meta-val.meta-highlight {
      color: #0284c7;
      font-weight: 700;
    }

    /* 左轨常驻原币汇总小计 */
    .rail-currency-sub-bar {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 4px 8px;
      margin-top: 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
    }

    .rail-currency-title {
      font-size: 11px;
      font-weight: 600;
      color: #475569;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
    }

    .rail-currency-chips {
      display: flex;
      align-items: center;
      gap: 4px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .rail-curr-chip {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      padding: 0 5px;
      border-radius: 3px;
      font-size: 11px;
    }

    .chip-curr {
      font-size: 9.5px;
      color: #64748b;
      font-weight: 700;
    }

    .chip-num {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-weight: 700;
      color: #0f172a;
    }

    .table-row-curr-breakdown {
      display: flex;
      gap: 4px;
      flex-wrap: wrap;
      justify-content: flex-end;
      margin-top: 2px;
    }

    .row-curr-tag {
      font-size: 10.5px;
      color: #64748b;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: #f1f5f9;
      padding: 0 4px;
      border-radius: 3px;
    }
`;

if (!content.includes('.settlement-currency-summary-bar')) {
  content = content.replace(cssMarker, newCss + '\n    ' + cssMarker);
}

// 2. Left Rail: Add rail-currency-sub-bar right under rail-metric-grid
const leftRailMetricMarker = `<div class="split-bar-track" style="margin-top: 8px;">`;
const leftRailCurrencyBar = `<!-- 各原币核销合计 (常驻底账即时可见) -->
                  <div v-if="settledOriginalCurrencyTotals.length > 0" class="rail-currency-sub-bar">
                    <div class="rail-currency-title">
                      <iconify-icon icon="ant-design:wallet-outlined" style="color: #0284c7;"></iconify-icon>
                      <span>核销原币合计:</span>
                    </div>
                    <div class="rail-currency-chips">
                      <span v-for="c in settledOriginalCurrencyTotals" :key="c.currency" class="rail-curr-chip">
                        <span class="chip-curr">{{ c.currency }}</span>
                        <b class="chip-num">{{ c.formatted }}</b>
                      </span>
                    </div>
                  </div>

                  <div class="split-bar-track" style="margin-top: 8px;">`;

if (!content.includes('class="rail-currency-sub-bar"')) {
  content = content.replace(leftRailMetricMarker, leftRailCurrencyBar);
}

// 3. Right Canvas: Add settlement-currency-summary-bar right above a-table
const rightCanvasTableMarker = `<a-table
                  v-else
                  :data-source="settlementListFiltered"`;

const rightCanvasSummaryBar = `<!-- 所有核销多原币合计看板横幅 (Multi-Currency Aggregate Banner) -->
                <div v-if="settlementListFiltered.length > 0" class="settlement-currency-summary-bar">
                  <div class="summary-bar-left">
                    <div class="summary-bar-badge">
                      <iconify-icon icon="ant-design:global-outlined" style="color: #1677ff; font-size: 14px;"></iconify-icon>
                      <span>所有核销原币合计：</span>
                    </div>
                    <div class="summary-currency-pills">
                      <div
                        v-for="item in settledOriginalCurrencyTotals"
                        :key="item.currency"
                        class="summary-curr-tag"
                        :class="'tag-curr-' + item.currency.toLowerCase()"
                        :title="'原币：' + item.currency + '，所有已核明细小计：' + item.formatted"
                      >
                        <span class="curr-symbol-badge">{{ item.currency }}</span>
                        <span class="curr-amount-val">{{ item.formatted }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="summary-bar-right">
                    <span class="summary-meta-item">
                      <span class="meta-lbl">核销单:</span>
                      <b class="meta-val">{{ settlementListFiltered.length }} 张 ({{ totalFeeItemCount }} 条明细)</b>
                    </span>
                    <span class="summary-meta-sep">|</span>
                    <span class="summary-meta-item">
                      <span class="meta-lbl">折合流水币总额:</span>
                      <b class="meta-val meta-highlight">{{ formatMoney(currentSettledAmount) }}</b>
                    </span>
                    <span class="summary-meta-sep">|</span>
                    <span class="summary-meta-item">
                      <span class="meta-lbl">折算差值:</span>
                      <b class="meta-val" :style="{ color: Math.abs(totalDiffAmount) > 0.005 ? '#d97706' : '#64748b' }">
                        {{ formatMoney(totalDiffAmount) }}
                      </b>
                    </span>
                  </div>
                </div>

                <a-table
                  v-else
                  :data-source="settlementListFiltered"`;

if (!content.includes('class="settlement-currency-summary-bar"')) {
  content = content.replace(rightCanvasTableMarker, rightCanvasSummaryBar);
}

// 4. Update settlement table row actualSettled to show that settlement's original currencies
const actualSettledCellMarker = `<template v-else-if="column.key === 'actualSettled'">
                      <span class="amount-cell-number amount-cell-emphasis">
                        {{ formatMoney(record.actualSettled) }}
                      </span>
                    </template>`;

const newActualSettledCell = `<template v-else-if="column.key === 'actualSettled'">
                      <span class="amount-cell-number amount-cell-emphasis">
                        {{ formatMoney(record.actualSettled) }}
                      </span>
                      <div class="table-row-curr-breakdown" :title="'本单原币合计：' + getSettlementOriginalCurrencies(record).map(c => c.currency + ' ' + c.formatted).join(' + ')">
                        <span v-for="c in getSettlementOriginalCurrencies(record)" :key="c.currency" class="row-curr-tag">
                          {{ c.currency }} {{ c.formatted }}
                        </span>
                      </div>
                    </template>`;

content = content.replace(actualSettledCellMarker, newActualSettledCell);

// 5. Update expanded header bar for fee items to show that settlement's original currencies
const expandedHeaderMarker = `<span class="amount-cell-number" style="color: #0284c7;">
                          本次结算小计: {{ formatMoney(record.actualSettled) }}
                        </span>`;

const newExpandedHeader = `<span style="margin-left: auto; display: flex; align-items: center; gap: 12px;">
                          <span style="font-size: 11px; color: #64748b;">
                            本单原币:
                            <span v-for="c in getSettlementOriginalCurrencies(record)" :key="c.currency" style="margin-left: 5px; font-weight: 700; color: #1e293b; font-family: monospace;">
                              {{ c.currency }} {{ c.formatted }}
                            </span>
                          </span>
                          <span class="amount-cell-number" style="color: #0284c7;">
                            本次结算小计: {{ formatMoney(record.actualSettled) }}
                          </span>
                        </span>`;

content = content.replace(expandedHeaderMarker, newExpandedHeader);

// 6. In preset_done, make fee_1 USD to showcase multi-currency aggregation in realistic freight forwarding!
const fee1Old = `{ id: 'fee_1', orderNo: 'QD261019001', masterBl: 'MSK9283719', etd: '2026-10-21', pol: '青岛', pod: '长滩', container: '2*40HQ', carrier: 'MSK', opName: '孙立', saleName: '赵明', feeName: '海运费 (O/F)', paySide: 1, feeCurrency: 'RMB', settledAmount: 350.00, exchangeRate: 1.000000, originalSettledAmount: 350.00 },`;
const fee1New = `{ id: 'fee_1', orderNo: 'QD261019001', masterBl: 'MSK9283719', etd: '2026-10-21', pol: '青岛', pod: '长滩', container: '2*40HQ', carrier: 'MSK', opName: '孙立', saleName: '赵明', feeName: '海运费 (O/F)', paySide: 1, feeCurrency: 'USD', settledAmount: 50.00, exchangeRate: 7.000000, originalSettledAmount: 350.00 },`;

if (content.includes(fee1Old)) {
  content = content.replace(fee1Old, fee1New);
}

// 7. Add computed properties in JS
const computedMarker = `// 统计关联核销明细与费用总条数
        const totalFeeItemCount = computed(() => {`;

const newComputedCode = `// --------------------------------------------------------------------
        // 3.1 所有核销单各原币别金额汇总 (Multi-Currency Settlement Totals)
        // --------------------------------------------------------------------
        function getCurrencySymbol(curr) {
          if (!curr) return '¥';
          const c = String(curr).toUpperCase();
          if (c === 'USD') return '$';
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
        const totalFeeItemCount = computed(() => {`;

if (!content.includes('settledOriginalCurrencyTotals = computed')) {
  content = content.replace(computedMarker, newComputedCode);
}

// 8. Return in setup
const returnMarker = `return {
          isCreateMode,`;

const newReturn = `return {
          settledOriginalCurrencyTotals,
          totalDiffAmount,
          getSettlementOriginalCurrencies,
          isCreateMode,`;

if (!content.includes('settledOriginalCurrencyTotals,')) {
  content = content.replace(returnMarker, newReturn);
}

fs.writeFileSync(targetFile, content, 'utf8');
console.log('Successfully added multi-currency original totals everywhere!');
