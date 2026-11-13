# coding: utf-8
import re

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check if getStatusIcon, getFeeAuditColor, getSettlementStatusColor, activeRightTab exist in script
script_start = content.find('<script>')
script_content = content[script_start:]

# Let's ensure these helper functions exist in script
helpers_to_add = """
        const activeRightTab = ref('timeline');

        const getStatusIcon = (status) => {
          switch (status) {
            case 0: return 'ant-design:edit-outlined';
            case 1: return 'ant-design:sync-outlined';
            case 2: return 'ant-design:close-circle-outlined';
            case 3: return 'ant-design:check-circle-outlined';
            case 4: return 'ant-design:pie-chart-outlined';
            case 5: return 'ant-design:safety-certificate-outlined';
            default: return 'ant-design:question-circle-outlined';
          }
        };

        const getFeeAuditColor = (status) => {
          if (status === '已审核') return 'success';
          if (status === '审核中') return 'processing';
          return 'default';
        };

        const getSettlementStatusColor = (status) => {
          if (status === '已结' || status === '结算完毕') return 'cyan';
          if (status === '部分结') return 'warning';
          return 'default';
        };

        const canSubmit = computed(() => {
          return formState.status === 0 || formState.status === 2;
        });

        const handleCreateBlank = () => {
          antd.message.info('已开启新空白付款申请凭证');
          switchScenario('S1');
        };

        const handleSaveDraft = () => {
          antd.message.success('草稿已成功保存至本地金融台账');
          isMainFormDirty.value = false;
        };

        const handleSubmitAudit = () => {
          antd.message.success('付款申请单已重新提交财务审批流！');
          formState.status = 1;
        };

        const handleWithdrawAudit = () => {
          antd.message.warning('已撤回审批申请，单据状态重置为录入中');
          formState.status = 0;
        };

        const handleExportAction = ({ key }) => {
          antd.message.success('正在导出 ' + key + ' 财务对账凭证件...');
        };

        const handlePrintDoc = () => {
          antd.message.info('正在调起凭证打印模版...');
          window.print();
        };

        const downloadAttachment = (att) => {
          antd.message.success('正在下载凭证文件: ' + (att.name || '附件'));
        };

        const removeDocAttachment = (id) => {
          antd.message.success('已删除单据附件');
        };
"""

# Let's check where to inject helpers into setup()
idx_setup_body = content.find('const isMainFormEditable = computed')
if 'const getStatusIcon =' not in content:
    content = content[:idx_setup_body] + helpers_to_add + "\n" + content[idx_setup_body:]

# Let's ensure they are returned from setup()
idx_return = content.rfind('return {')
return_inject = """          activeRightTab,
          getStatusIcon,
          getFeeAuditColor,
          getSettlementStatusColor,
          canSubmit,
          handleCreateBlank,
          handleSaveDraft,
          handleSubmitAudit,
          handleWithdrawAudit,
          handleExportAction,
          handlePrintDoc,
          downloadAttachment,
          removeDocAttachment,
"""
if 'getStatusIcon,' not in content[idx_return:]:
    content = content[:idx_return + 8] + "\n" + return_inject + content[idx_return + 8:]

with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected helper functions and returns successfully.")
