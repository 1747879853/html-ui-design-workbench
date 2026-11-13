# coding: utf-8

with open('pages/payment-application-edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix scenario bar
text = text.replace(
    'v-for="s in presetScenarios"',
    'v-for="s in scenarioList"'
).replace(
    ':key="s.id"',
    ':key="s.key"'
).replace(
    'currentScenarioId === s.id',
    'currentScenarioKey === s.key'
).replace(
    '@click="switchScenario(s.id)"',
    '@click="switchScenario(s.key)"'
).replace(
    '[{{ s.docCode }}]',
    '[{{ s.docNo }}]'
).replace(
    'v-model:checked="simulateSendFailure"',
    'v-model:checked="simulateSubmitStepFail"'
).replace(
    '@click="showHandoffDocModal = true"',
    '@click="showHandoffDrawer = true"'
).replace(
    'showFieldFixModal = true',
    'showAddFeeDrawer = true'
)

# Fix docCode / applicantName / statusName
text = text.replace(
    '{{ formState.docCode }}',
    '{{ formState.applicationNo }}'
).replace(
    "copyText(formState.docCode, '申请单号')",
    "copyText(formState.applicationNo, '申请单号')"
).replace(
    '{{ formState.applicantName }}',
    '{{ formState.creatorUserName }}'
).replace(
    '{{ formState.statusName }}',
    '{{ currentStatusMeta.stampText }}'
)

# Fix rejection banner
rejection_old = """      <!-- S3 已驳回：置顶强视觉警示横幅 -->
      <div v-if="formState.status === 2" class="pa-status-callout callout-rejected">
        <div style="display: flex; align-items: center; gap: 8px;">
          <iconify-icon icon="ant-design:close-circle-filled" style="color: #dc2626; font-size: 14px; flex-shrink: 0;"></iconify-icon>
          <strong style="color: #991b1b; white-space: nowrap;">审批已驳回 ({{ auditTimeline[1]?.operator || '张财务' }} · {{ auditTimeline[1]?.time || '2026-10-30 11:45' }})：</strong>
          <span style="color: #b91c1c;">{{ auditTimeline[1]?.comment || 'GH137测试结束：恢复原专用申请至驳回状态，请补充水单盖章件后重提。' }}</span>
        </div>
        <a-tag color="error" style="font-size: 10px; line-height: 18px; margin: 0; flex-shrink: 0;">需修改后重新送审</a-tag>
      </div>"""

rejection_new = """      <!-- S3 已驳回：置顶强视觉警示横幅 -->
      <div v-if="formState.status === 2" class="pa-status-callout callout-rejected">
        <div style="display: flex; align-items: center; gap: 8px;">
          <iconify-icon icon="ant-design:close-circle-filled" style="color: #dc2626; font-size: 14px; flex-shrink: 0;"></iconify-icon>
          <strong style="color: #991b1b; white-space: nowrap;">审批已驳回 ({{ (workflowNodes[1] || {}).operatorName || '张财务' }} · {{ (workflowNodes[1] || {}).operateTime || '2026-10-30 11:45' }})：</strong>
          <span style="color: #b91c1c;">{{ (workflowNodes[1] || {}).comment || 'GH137测试结束：恢复原专用申请至驳回状态，请补充水单盖章件后重提。' }}</span>
        </div>
        <a-tag color="error" style="font-size: 10px; line-height: 18px; margin: 0; flex-shrink: 0;">需修改后重新送审</a-tag>
      </div>"""

text = text.replace(rejection_old, rejection_new)

# Fix right card timeline & attachments
timeline_old = """            <!-- 标签页 1：审批流转跟踪 -->
            <div v-if="activeRightTab === 'timeline'" class="pa-timeline-box">
              <div
                v-for="node in auditTimeline"
                :key="node.nodeId"
                class="pa-node-card"
                :class="{ 'is-reject': node.status === 'rejected', 'is-pass': node.status === 'passed' }"
              >
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <iconify-icon
                      :icon="node.status === 'passed' ? 'ant-design:check-circle-filled' : (node.status === 'rejected' ? 'ant-design:close-circle-filled' : 'ant-design:clock-circle-outlined')"
                      :style="{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#94a3b8'), fontSize: '14px' }"
                    ></iconify-icon>
                    <strong style="color: #0f172a;">{{ node.nodeName }}</strong>
                  </div>
                  <span
                    :style="{
                      fontSize: '10px',
                      padding: '1px 5px',
                      borderRadius: '3px',
                      background: node.status === 'passed' ? '#dcfce7' : (node.status === 'rejected' ? '#fee2e2' : '#f1f5f9'),
                      color: node.status === 'passed' ? '#15803d' : (node.status === 'rejected' ? '#b91c1c' : '#64748b'),
                      fontWeight: 600
                    }"
                  >
                    {{ node.status === 'passed' ? '已提交' : (node.status === 'rejected' ? '已驳回' : '未到达') }}
                  </span>
                </div>

                <div style="margin-top: 3px; color: #64748b; font-size: 10px; display: flex; align-items: center; justify-content: space-between;">
                  <span>处理人: {{ node.operator }}</span>
                  <span class="tabular-nums">{{ node.time }}</span>
                </div>

                <div v-if="node.comment" style="margin-top: 4px; padding: 3px 6px; border-radius: 3px; font-size: 11px;" :style="{ background: node.status === 'rejected' ? '#fee2e2' : '#ffffff', color: node.status === 'rejected' ? '#991b1b' : '#334155' }">
                  <strong v-if="node.status === 'rejected'">驳回原因: </strong>
                  <span v-else>意见: </span>
                  {{ node.comment }}
                </div>

                <div v-if="node.hasSignature" style="margin-top: 4px; display: flex; justify-content: flex-end;">
                  <span class="pa-seal-badge">
                    <iconify-icon icon="ant-design:safety-outlined"></iconify-icon>
                    电子签名: {{ node.operator }}
                  </span>
                </div>
              </div>
            </div>

            <!-- 标签页 2：单据档案与附件池 -->
            <div v-else style="padding: 4px 6px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #64748b; font-size: 11px;">单据归档清单 (支持发票扫描件、水单、货权凭证)</span>
                <a-upload :show-upload-list="false" :before-upload="handleUploadDocAttachment">
                  <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 6px;">
                    + 上传单据附件
                  </a-button>
                </a-upload>
              </div>

              <div
                v-for="att in docAttachmentList"
                :key="att.id"
                style="display: flex; align-items: center; justify-content: space-between; padding: 4px 6px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; margin-bottom: 4px;"
              >
                <div style="display: flex; align-items: center; gap: 6px; overflow: hidden;">
                  <iconify-icon icon="ant-design:file-pdf-outlined" style="color: #dc2626; font-size: 14px; flex-shrink: 0;"></iconify-icon>
                  <span style="font-size: 11px; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" :title="att.name">
                    {{ att.name }}
                  </span>
                  <span style="font-size: 10px; color: #94a3b8; font-family: monospace;">({{ att.size }})</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                  <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="previewAttachment(att)">预览</a-button>
                  <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="downloadAttachment(att)">下载</a-button>
                  <a-button type="link" size="small" danger style="font-size: 11px; padding: 0;" @click="removeDocAttachment(att.id)">删</a-button>
                </div>
              </div>

              <div v-if="docAttachmentList.length === 0" style="text-align: center; color: #94a3b8; padding: 20px;">
                暂无归档附件
              </div>
            </div>"""

timeline_new = """            <!-- 标签页 1：审批流转跟踪 -->
            <div v-if="activeRightTab === 'timeline'" class="pa-timeline-box">
              <div
                v-for="node in workflowNodes"
                :key="node.nodeName"
                class="pa-node-card"
                :class="{ 'is-reject': node.status === 'rejected', 'is-pass': node.status === 'passed' }"
              >
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <iconify-icon
                      :icon="node.status === 'passed' ? 'ant-design:check-circle-filled' : (node.status === 'rejected' ? 'ant-design:close-circle-filled' : 'ant-design:clock-circle-outlined')"
                      :style="{ color: node.status === 'passed' ? '#16a34a' : (node.status === 'rejected' ? '#dc2626' : '#94a3b8'), fontSize: '14px' }"
                    ></iconify-icon>
                    <strong style="color: #0f172a;">{{ node.nodeName }}</strong>
                  </div>
                  <span
                    :style="{
                      fontSize: '10px',
                      padding: '1px 5px',
                      borderRadius: '3px',
                      background: node.status === 'passed' ? '#dcfce7' : (node.status === 'rejected' ? '#fee2e2' : '#f1f5f9'),
                      color: node.status === 'passed' ? '#15803d' : (node.status === 'rejected' ? '#b91c1c' : '#64748b'),
                      fontWeight: 600
                    }"
                  >
                    {{ node.statusText || (node.status === 'passed' ? '已提交' : (node.status === 'rejected' ? '已驳回' : '未到达')) }}
                  </span>
                </div>

                <div style="margin-top: 3px; color: #64748b; font-size: 10px; display: flex; align-items: center; justify-content: space-between;">
                  <span>处理人: {{ node.operatorName }}</span>
                  <span class="tabular-nums">{{ node.operateTime }}</span>
                </div>

                <div v-if="node.comment" style="margin-top: 4px; padding: 3px 6px; border-radius: 3px; font-size: 11px;" :style="{ background: node.status === 'rejected' ? '#fee2e2' : '#ffffff', color: node.status === 'rejected' ? '#991b1b' : '#334155' }">
                  <strong v-if="node.status === 'rejected'">驳回原因: </strong>
                  <span v-else>意见: </span>
                  {{ node.comment }}
                </div>

                <div v-if="node.signature" style="margin-top: 4px; display: flex; justify-content: flex-end;">
                  <span class="pa-seal-badge">
                    <iconify-icon icon="ant-design:safety-outlined"></iconify-icon>
                    电子签名: {{ node.signature }}
                  </span>
                </div>
              </div>
            </div>

            <!-- 标签页 2：单据档案与附件池 -->
            <div v-else style="padding: 4px 6px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #64748b; font-size: 11px;">单据归档清单 (支持发票扫描件、水单、货权凭证)</span>
                <a-upload :show-upload-list="false" :before-upload="handleUploadApplicationAttachment">
                  <a-button size="small" type="primary" ghost style="font-size: 10px; height: 20px; padding: 0 6px;">
                    + 上传单据附件
                  </a-button>
                </a-upload>
              </div>

              <div v-for="grp in applicationAttachmentGroups" :key="grp.groupName" style="margin-bottom: 6px;">
                <div style="font-weight: 600; color: #475569; font-size: 10px; margin-bottom: 2px;">{{ grp.groupName }} ({{ grp.items.length }})</div>
                <div
                  v-for="att in grp.items"
                  :key="att.name"
                  style="display: flex; align-items: center; justify-content: space-between; padding: 3px 6px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 3px; margin-bottom: 2px;"
                >
                  <div style="display: flex; align-items: center; gap: 6px; overflow: hidden;">
                    <iconify-icon icon="ant-design:file-pdf-outlined" style="color: #dc2626; font-size: 13px; flex-shrink: 0;"></iconify-icon>
                    <span style="font-size: 11px; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" :title="att.name">
                      {{ att.name }}
                    </span>
                    <span style="font-size: 10px; color: #94a3b8; font-family: monospace;">({{ att.sizeText || '1.2 MB' }})</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="previewAttachment(att)">预览</a-button>
                    <a-button type="link" size="small" style="font-size: 11px; padding: 0;" @click="downloadAttachment(att)">下载</a-button>
                    <a-button type="link" size="small" danger style="font-size: 11px; padding: 0;" @click="removeApplicationAttachment(att)">删</a-button>
                  </div>
                </div>
              </div>
            </div>"""

text = text.replace(timeline_old, timeline_new)

# Fix footer auditTimeline
text = text.replace(
    "最后流转: {{ auditTimeline[auditTimeline.length - 1]?.time || '2026-10-30 11:45:00' }}",
    "最后流转: {{ (workflowNodes[workflowNodes.length - 1] || {}).operateTime || '2026-10-30 11:45:00' }}"
)

# Fix docAttachmentList.length
text = text.replace(
    "单据档案 ({{ docAttachmentList.length }})",
    "单据档案 ({{ applicationAttachmentGroups.reduce((acc, g) => acc + g.items.length, 0) }})"
)

with open('pages/payment-application-edit.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Template bindings fixed successfully.")
