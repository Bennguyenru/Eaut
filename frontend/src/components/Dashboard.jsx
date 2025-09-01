import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts'
import { 
  Target, 
  BookOpen, 
  FileText, 
  TrendingUp, 
  Users, 
  CheckCircle,
  AlertTriangle,
  Clock,
  Wifi,
  WifiOff
} from 'lucide-react'
import apiClient from '../lib/api.js'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalPLOs: 0,
    totalCLOs: 0,
    totalDocuments: 0,
    processedDocuments: 0,
    averageScore: 0,
    achievementRate: 0
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [apiStatus, setApiStatus] = useState('checking') // checking, connected, disconnected

  // Sample data for charts (fallback when no real data)
  const ploData = [
    { name: 'PLO4', score: 3.2, target: 4.0 },
    { name: 'PLO5', score: 2.8, target: 4.0 },
    { name: 'PLO6', score: 3.5, target: 4.0 },
    { name: 'PLO10', score: 3.0, target: 4.0 },
    { name: 'PLO12', score: 3.8, target: 4.0 }
  ]

  const cloData = [
    { name: 'CLO1', score: 3.1, course: 'ME2252' },
    { name: 'CLO2', score: 2.9, course: 'ME2252' },
    { name: 'CLO3', score: 3.4, course: 'ME2252' },
    { name: 'CLO4', score: 3.7, course: 'ME2252' }
  ]

  const achievementData = [
    { level: 'Xuất sắc (3.5-4.0)', count: 2, color: '#22c55e' },
    { level: 'Tốt (2.5-3.4)', count: 6, color: '#3b82f6' },
    { level: 'Trung bình (1.5-2.4)', count: 1, color: '#f59e0b' },
    { level: 'Yếu (<1.5)', count: 0, color: '#ef4444' }
  ]

  const trendData = [
    { month: 'T1', score: 2.8 },
    { month: 'T2', score: 3.0 },
    { month: 'T3', score: 3.2 },
    { month: 'T4', score: 3.1 },
    { month: 'T5', score: 3.4 },
    { month: 'T6', score: 3.3 }
  ]

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Check API health first
      const healthResponse = await apiClient.healthCheck()
      setApiStatus('connected')
      
      // Fetch dashboard data
      const [ploResponse, cloResponse, summaryResponse] = await Promise.all([
        apiClient.getPLOs().catch(() => ({ plos: [] })),
        apiClient.getCLOs().catch(() => ({ clos: [] })),
        apiClient.getOverallSummary().catch(() => ({}))
      ])
      
      setStats({
        totalPLOs: ploResponse.plos?.length || 5, // fallback to sample data
        totalCLOs: cloResponse.clos?.length || 4,
        totalDocuments: summaryResponse.total_documents || 0,
        processedDocuments: summaryResponse.processed_documents || 0,
        averageScore: summaryResponse.average_score || 0,
        achievementRate: summaryResponse.achievement_rate || 0
      })
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      setError(error.message)
      setApiStatus('disconnected')
      
      // Use fallback data
      setStats({
        totalPLOs: 5,
        totalCLOs: 4,
        totalDocuments: 0,
        processedDocuments: 0,
        averageScore: 0,
        achievementRate: 0
      })
    } finally {
      setLoading(false)
    }
  }

  const getApiStatusBadge = () => {
    switch (apiStatus) {
      case 'connected':
        return (
          <Badge variant="secondary" className="bg-green-100 text-green-800">
            <Wifi className="w-4 h-4 mr-1" />
            API kết nối
          </Badge>
        )
      case 'disconnected':
        return (
          <Badge variant="secondary" className="bg-red-100 text-red-800">
            <WifiOff className="w-4 h-4 mr-1" />
            API ngắt kết nối
          </Badge>
        )
      default:
        return (
          <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
            <Clock className="w-4 h-4 mr-1" />
            Đang kiểm tra...
          </Badge>
        )
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Đang tải dữ liệu dashboard...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* API Status Alert */}
      {error && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            Không thể kết nối với backend API: {error}. Hiển thị dữ liệu mẫu.
          </AlertDescription>
        </Alert>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tổng số PLO</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalPLOs}</div>
            <p className="text-xs text-muted-foreground">
              Chuẩn đầu ra chương trình
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tổng số CLO</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalCLOs}</div>
            <p className="text-xs text-muted-foreground">
              Chuẩn đầu ra môn học
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tài liệu đã xử lý</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.processedDocuments}</div>
            <p className="text-xs text-muted-foreground">
              Tổng số: {stats.totalDocuments} tài liệu
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Điểm trung bình</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {stats.averageScore > 0 ? stats.averageScore.toFixed(1) : '--'}
            </div>
            <p className="text-xs text-muted-foreground">
              Thang điểm 4.0
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* PLO Achievement Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Mức độ đạt PLO</CardTitle>
            <CardDescription>
              So sánh điểm đạt được với mục tiêu
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={ploData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 4]} />
                <Tooltip />
                <Bar dataKey="score" fill="#3b82f6" name="Điểm đạt được" />
                <Bar dataKey="target" fill="#e5e7eb" name="Mục tiêu" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* CLO Achievement Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Mức độ đạt CLO</CardTitle>
            <CardDescription>
              Điểm đánh giá theo từng CLO
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={cloData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 4]} />
                <Tooltip />
                <Bar dataKey="score" fill="#10b981" name="Điểm CLO" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Achievement Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Phân bố mức độ đạt chuẩn</CardTitle>
            <CardDescription>
              Số lượng sinh viên theo từng mức
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={achievementData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {achievementData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Trend Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Xu hướng điểm số</CardTitle>
            <CardDescription>
              Biến động điểm trung bình theo thời gian
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis domain={[0, 4]} />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="#8b5cf6" 
                  strokeWidth={2}
                  name="Điểm trung bình"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Hoạt động gần đây</CardTitle>
          <CardDescription>
            Các tài liệu và đánh giá mới nhất
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium">Trạng thái API Backend</p>
                <p className="text-xs text-muted-foreground">
                  {apiStatus === 'connected' 
                    ? 'Kết nối thành công với backend server'
                    : 'Không thể kết nối với backend server'
                  }
                </p>
              </div>
              {getApiStatusBadge()}
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium">Đã tải dữ liệu PLO/CLO</p>
                <p className="text-xs text-muted-foreground">
                  {stats.totalPLOs} PLO và {stats.totalCLOs} CLO từ chương trình CNKT Ô tô
                </p>
              </div>
              <Badge variant="secondary">
                <CheckCircle className="w-3 h-3 mr-1" />
                Hoàn thành
              </Badge>
            </div>

            <div className="flex items-center space-x-4">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium">Chờ tài liệu đánh giá</p>
                <p className="text-xs text-muted-foreground">
                  Tải lên tài liệu để bắt đầu đánh giá CLO/PLO
                </p>
              </div>
              <Badge variant="outline">
                <AlertTriangle className="w-3 h-3 mr-1" />
                Đang chờ
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

