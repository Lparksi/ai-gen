<template>
  <div class="diary-list">
    <el-header>
      <el-row :gutter="20" class="header-row">
        <el-col :span="12">
          <h1>我的日记</h1>
        </el-col>
        <el-col :span="12" class="header-buttons">
          <el-input v-model="searchQuery" placeholder="搜索日记..." @input="searchDiaries" style="width: 200px; margin-right: 10px;"></el-input>
          <el-button type="primary" @click="goToEdit">新增日记</el-button>
          <el-button type="success" @click="addDemoData">添加演示数据</el-button>
          <el-button type="default" @click="toggleDarkMode">{{ darkMode ? '关闭黑暗模式' : '开启黑暗模式' }}</el-button>
          <el-button type="danger" @click="showDeleteSelectedDialog" :disabled="selectedDiaries.length === 0" style="margin-left: 10px;">删除选中</el-button>
          <el-button type="danger" @click="showDeleteAllDialog" style="margin-left: 10px;">全部删除</el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-dialog title="确认删除" v-model="deleteSelectedDialogVisible" width="30%">
        <span>您确定要删除选中的 {{ selectedDiaries.length }} 条日记吗？此操作无法撤销。</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="deleteSelectedDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deleteSelectedDiaries">确认删除</el-button>
        </span>
      </el-dialog>
      <el-dialog title="确认删除全部" v-model="deleteAllDialogVisible" width="30%">
        <span>您确定要删除所有日记吗？此操作无法撤销。</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="deleteAllDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="deleteAllDiaries">确认删除全部</el-button>
        </span>
      </el-dialog>
      <el-row :gutter="20">
        <el-col :span="6" class="sidebar">
          <el-card class="filter-card">
            <h3>筛选</h3>
            <el-divider></el-divider>
            <h4>心情</h4>
            <el-checkbox-group v-model="selectedMoods" @change="filterDiaries">
              <el-checkbox v-for="mood in moods" :key="mood" :value="mood">{{ mood }}</el-checkbox>
            </el-checkbox-group>
            <el-divider></el-divider>
            <h4>标签</h4>
            <el-checkbox-group v-model="selectedTags" @change="filterDiaries">
              <el-checkbox v-for="tag in tags" :key="tag" :value="tag">{{ tag }}</el-checkbox>
            </el-checkbox-group>
          </el-card>
        </el-col>
        <el-col :span="18">
          <div class="card-view">
            <el-card v-for="diary in filteredDiaries" :key="diary[0]" class="diary-card" @click.native="goToDetail(diary[0])" :class="{ 'selected': selectedDiaries.includes(diary[0]) }">
              <div style="display: flex; align-items: center;">
                <el-checkbox :value="selectedDiaries.includes(diary[0])" @change="toggleDiarySelection(diary[0])" @click.native.stop class="diary-checkbox-left"></el-checkbox>
                <div>
                  <h3>{{ diary[1] }}</h3>
                  <p class="date">{{ formatDate(diary[7]) }}</p>
                  <p class="content">{{ truncateContent(diary[2]) }}</p>
                  <p class="mood">心情：{{ diary[3] }}</p>
                  <p class="tags">标签：{{ diary[4] }}</p>
                </div>
              </div>
            </el-card>
          </div>
          <el-empty v-if="filteredDiaries.length === 0" description="暂无日记"></el-empty>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DiaryList',
  data() {
    return {
      diaries: [],
      filteredDiaries: [],
      searchQuery: '',
      selectedMoods: [],
      selectedTags: [],
      selectedDiaries: [],
      moods: ['开心', '难过', '平静', '愤怒', '焦虑'],
      tags: ['工作', '生活', '旅行', '学习', '家庭', '朋友'],
      darkMode: localStorage.getItem('darkMode') === 'true',
      deleteSelectedDialogVisible: false,
      deleteAllDialogVisible: false
    }
  },
  mounted() {
    this.fetchDiaries()
    this.applyTheme()
  },
  methods: {
    fetchDiaries() {
      axios.get('/api/diaries').then(response => {
        this.diaries = response.data
        this.filteredDiaries = response.data
      }).catch(error => {
        console.error('Error fetching diaries:', error)
      })
    },
    searchDiaries() {
      if (this.searchQuery) {
        axios.get(`/api/search?query=${this.searchQuery}`).then(response => {
          this.filteredDiaries = response.data
        }).catch(error => {
          console.error('Error searching diaries:', error)
        })
      } else {
        this.filteredDiaries = this.diaries
      }
      this.filterDiaries()
    },
    filterDiaries() {
      let filtered = this.diaries
      if (this.selectedMoods.length > 0) {
        filtered = filtered.filter(diary => this.selectedMoods.includes(diary[3]))
      }
      if (this.selectedTags.length > 0) {
        filtered = filtered.filter(diary => {
          const tags = diary[4].split(',')
          return this.selectedTags.some(tag => tags.includes(tag))
        })
      }
      this.filteredDiaries = filtered
    },
    goToDetail(id) {
      this.$router.push({ name: 'DiaryDetail', params: { id } })
    },
    goToEdit() {
      this.$router.push({ name: 'DiaryEdit' })
    },
    addDemoData() {
      axios.post('/api/demo-data').then(() => {
        this.$message.success('演示数据添加成功')
        this.fetchDiaries()
      }).catch(error => {
        console.error('Error adding demo data:', error)
        this.$message.error('添加演示数据失败')
      })
    },
    changeView(command) {
      this.viewMode = command
      localStorage.setItem('viewMode', this.viewMode)
    },
    toggleDiarySelection(id) {
      if (this.selectedDiaries.includes(id)) {
        this.selectedDiaries = this.selectedDiaries.filter(d => d !== id)
      } else {
        this.selectedDiaries.push(id)
      }
    },
    handleSelectionChange(val) {
      this.selectedDiaries = val.map(row => row[0])
    },
    tableRowClassName(row) {
      if (this.selectedDiaries.includes(row[0])) {
        return 'selected-row';
      }
      return '';
    },
    showDeleteSelectedDialog() {
      this.deleteSelectedDialogVisible = true
    },
    showDeleteAllDialog() {
      this.deleteAllDialogVisible = true
    },
    deleteSelectedDiaries() {
      axios.post('/api/diaries/bulk-delete', { ids: this.selectedDiaries }).then(() => {
        this.$message.success('删除成功')
        this.fetchDiaries()
        this.selectedDiaries = []
        this.deleteSelectedDialogVisible = false
      }).catch(error => {
        console.error('Error deleting diaries:', error)
        this.$message.error('删除失败')
      })
    },
    deleteAllDiaries() {
      axios.delete('/api/diaries/all').then(() => {
        this.$message.success('全部删除成功')
        this.fetchDiaries()
        this.deleteAllDialogVisible = false
      }).catch(error => {
        console.error('Error deleting all diaries:', error)
        this.$message.error('全部删除失败')
      })
    },
    goToDetailRow(row) {
      this.$router.push({ name: 'DiaryDetail', params: { id: row[0] } })
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
      this.applyTheme()
    },
    applyTheme() {
      if (this.darkMode) {
        document.body.classList.add('dark-mode')
      } else {
        document.body.classList.remove('dark-mode')
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
    },
    formatDateTable(row, column, cellValue) {
      const date = new Date(cellValue)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
    },
    truncateContent(content) {
      return content.length > 100 ? content.substring(0, 100) + '...' : content
    }
  }
}
</script>

<style scoped>
.diary-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
.header-row {
  display: flex;
  align-items: center;
}
.header-buttons {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
}
.filter-card {
  margin-bottom: 20px;
}
.diary-card {
  margin-bottom: 20px;
  cursor: pointer;
  text-align: left;
  position: relative;
}
.diary-card h3 {
  margin-top: 0;
}
.diary-checkbox-left {
  margin-right: 10px;
}
.selected {
  border: 2px solid #409EFF;
}
.date {
  color: #909399;
  font-size: 14px;
}
.content {
  color: #606266;
}
.mood, .tags {
  font-size: 14px;
  color: #909399;
}
.el-empty {
  margin-top: 50px;
}
@media (max-width: 768px) {
  .sidebar {
    position: relative;
    top: 0;
  }
  .el-row {
    display: block;
  }
  .el-col {
    width: 100%;
  }
  .header-buttons {
    justify-content: flex-start;
    margin-top: 10px;
  }
}
</style>

<style>
body.dark-mode {
  background-color: #121212;
  color: #e0e0e0;
}
body.dark-mode .diary-list h1,
body.dark-mode .diary-card h3,
body.dark-mode .filter-card h3,
body.dark-mode .filter-card h4 {
  color: #ffffff;
}
body.dark-mode .date,
body.dark-mode .mood,
body.dark-mode .tags {
  color: #b0b0b0;
}
body.dark-mode .content {
  color: #c0c0c0;
}
body.dark-mode .el-card {
  background-color: #1e1e1e;
  border: 1px solid #333;
}
body.dark-mode .el-dialog {
  background-color: #1e1e1e;
}
body.dark-mode .el-form-item label {
  color: #e0e0e0;
}
body.dark-mode .el-button {
  background-color: var(--theme-color);
  color: #ffffff;
}
body.dark-mode .el-button:hover {
  opacity: 0.8;
}
body.dark-mode .el-input__inner {
  background-color: #2d2d2d;
  border: 1px solid #444;
  color: #e0e0e0;
}
body.dark-mode .el-divider {
  background-color: #444;
}
</style>
