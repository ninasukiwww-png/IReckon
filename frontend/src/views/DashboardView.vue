<template>
  <div class="page-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">仪表盘</h1>
        <p class="page-subtitle">系统概览与运行状态</p>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-card card">
        <div class="stat-icon-box purple">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.totalTasks }}</span>
          <span class="stat-label">总任务数</span>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon-box yellow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.activeTasks }}</span>
          <span class="stat-label">进行中</span>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon-box green">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.completedTasks }}</span>
          <span class="stat-label">已完成</span>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon-box red">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 0 1 10 10c0 2.5-1 4.8-2.6 6.5"/><path d="M12 2a10 10 0 0 0-7.4 16.5"/><circle cx="12" cy="12" r="3"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.failedTasks }}</span>
          <span class="stat-label">失败</span>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon-box blue">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.aiInstances }}</span>
          <span class="stat-label">AI 实例</span>
        </div>
      </div>
    </div>

    <div class="panels-row">
      <div class="panel card">
        <h3 class="panel-title">系统状态</h3>
        <div class="system-info">
          <div class="info-row">
            <span class="info-label">版本</span>
            <span class="info-value">{{ health.version || '1.0.0' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">运行状态</span>
            <span class="info-value health-ok" v-if="health.status !== 'error'">
              <span class="status-dot on"></span> 正常运行
            </span>
            <span class="info-value health-err" v-else>
              <span class="status-dot off"></span> 异常
            </span>
          </div>
          <div class="info-row" v-if="health.uptime">
            <span class="info-label">运行时间</span>
            <span class="info-value">{{ health.uptime }}</span>
          </div>
        </div>
      </div>

      <div class="panel card">
        <h3 class="panel-title">最近活动</h3>
        <div class="activity-list">
          <div v-for="task in recentTasks" :key="task.task_id" class="activity-item">
            <span class="activity-dot" :class="statusDot(task.status)"></span>
            <span class="activity-text">{{ task.user_request?.slice(0, 36) || '无描述' }}</span>
            <span class="activity-time">{{ formatTime(task.updated_at) }}</span>
          </div>
          <div v-if="!recentTasks.length" class="activity-empty">暂无活动</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '../stores/taskStore.js'
import { healthAPI, aiInstanceAPI } from '../api/index.js'

const taskStore = useTaskStore()
const health = ref({})
const aiInstances = ref([])
const tasks = computed(() => taskStore.tasks)

const stats = computed(() => ({
  totalTasks: tasks.value.length,
  activeTasks: tasks.value.filter(t => t.status === 'executing').length,
  completedTasks: tasks.value.filter(t => t.status === 'completed').length,
  failedTasks: tasks.value.filter(t => t.status === 'failed').length,
  aiInstances: aiInstances.value.length
}))

const recentTasks = computed(() => tasks.value.slice(0, 6))

onMounted(async () => {
  await taskStore.fetchTasks()
  try {
    const [h, ai] = await Promise.all([healthAPI.check(), aiInstanceAPI.list()])
    health.value = h.data
    aiInstances.value = ai.data
  } catch {}
})

function statusDot(status) {
  const map = { completed: 'dot-green', failed: 'dot-red', executing: 'dot-yellow', pending: 'dot-gray' }
  return map[status] || 'dot-gray'
}

function formatTime(ts) {
  if (!ts) return '-'
  return new Date(ts).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.stats-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
}

.stat-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon-box.purple { background: rgba(var(--primary), 0.15); color: var(--primary); }
.stat-icon-box.yellow { background: rgba(245, 158, 11, 0.15); color: var(--warning); }
.stat-icon-box.green { background: rgba(16, 185, 129, 0.15); color: var(--success); }
.stat-icon-box.red { background: rgba(239, 68, 68, 0.15); color: var(--error); }
.stat-icon-box.blue { background: rgba(59, 130, 246, 0.15); color: var(--info); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
}

.panels-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-light);
}

.info-row:last-child { border-bottom: none; }

.info-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.info-value {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.on { background: var(--success); box-shadow: 0 0 6px var(--success); }
.status-dot.off { background: var(--error); }

.health-ok { color: var(--success); }
.health-err { color: var(--error); }

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}

.activity-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-green { background: var(--success); }
.dot-red { background: var(--error); }
.dot-yellow { background: var(--warning); }
.dot-gray { background: var(--text-muted); }

.activity-text {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.activity-time {
  font-size: 11px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.activity-empty {
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  padding: 16px;
}

@media (max-width: 1000px) {
  .stats-row { grid-template-columns: repeat(3, 1fr); }
  .panels-row { grid-template-columns: 1fr; }
}
</style>
