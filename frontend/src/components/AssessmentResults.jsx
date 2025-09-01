import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table.jsx'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line
} from 'recharts'
import { 
  FileText, 
  Download, 
  Eye, 
  Filter,
  Search,
  TrendingUp,
  Target,
  BarChart3,
  Calendar,
  User
} from 'lucide-react'

const AssessmentResults = () => {
  const [results, setResults] = useState([])
  const [filteredResults, setFilteredResults] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCourse, setSelectedCourse] = useState('all')
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [viewMode, setViewMode] = useState('list') // list, detail, analytics

  // Sample assessment results data
  const sampleResults = [
    {
      id: 1,
      document_name: 'Bài tập tuần 1 - Nguyễn Văn A.pdf',
      course_code: 'ME2252',
      course_name: 'Vẽ kỹ thuật',
      document_type: 'assignment',
      upload_date: '2024-01-15',
      student_name: 'Nguyễn Văn A',
      clo_scores: [
        { clo_code: 'CLO1', clo_title: 'Hiểu các hệ lực cơ học', score: 3.2, confidence: 0.85, max_score: 4.0 },
        { clo_code: 'CLO2', clo_title: 'Xây dựng mô hình lực', score: 2.8, confidence: 0.78, max_score: 4.0 },
        { clo_code: 'CLO3', clo_title: 'Phân tích và tính toán', score: 3.5, confidence: 0.92, max_score: 4.0 },
        { clo_code: 'CLO4', clo_title: 'Thái độ học tập', score: 3.8, confidence: 0.88, max_score: 4.0 }
      ],
      plo_scores: [
        { plo_code: 'PLO4', plo_title: 'Áp dụng kiến thức kỹ thuật', score: 3.0, confidence: 0.82 },
        { plo_code: 'PLO10', plo_title: 'Đọc hiểu bản vẽ kỹ thuật', score: 3.5, confidence: 0.92 },
        { plo_code: 'PLO12', plo_title: 'Phẩm chất đạo đức nghề nghiệp', score: 3.8, confidence: 0.88 }
      ],
      overall_score: 3.3,
      achievement_level: 'Tốt'
    },
    {
      id: 2,
      document_name: 'Bài kiểm tra giữa kỳ - Trần Thị B.pdf',
      course_code: 'ME2252',
      course_name: 'Vẽ kỹ thuật',
      document_type: 'exam',
      upload_date: '2024-01-20',
      student_name: 'Trần Thị B',
      clo_scores: [
        { clo_code: 'CLO1', clo_title: 'Hiểu các hệ lực cơ học', score: 2.5, confidence: 0.75, max_score: 4.0 },
        { clo_code: 'CLO2', clo_title: 'Xây dựng mô hình lực', score: 2.2, confidence: 0.68, max_score: 4.0 },
        { clo_code: 'CLO3', clo_title: 'Phân tích và tính toán', score: 2.8, confidence: 0.82, max_score: 4.0 },
        { clo_code: 'CLO4', clo_title: 'Thái độ học tập', score: 3.5, confidence: 0.85, max_score: 4.0 }
      ],
      plo_scores: [
        { plo_code: 'PLO4', plo_title: 'Áp dụng kiến thức kỹ thuật', score: 2.35, confidence: 0.72 },
        { plo_code: 'PLO10', plo_title: 'Đọc hiểu bản vẽ kỹ thuật', score: 2.8, confidence: 0.82 },
        { plo_code: 'PLO12', plo_title: 'Phẩm chất đạo đức nghề nghiệp', score: 3.5, confidence: 0.85 }
      ],
      overall_score: 2.75,
      achievement_level: 'Trung bình'
    }
  ]

  const courses = [
    { code: 'ME2252', name: 'Vẽ kỹ thuật' },
    { code: 'ME2205', name: 'Cơ học kỹ thuật' },
    { code: 'AET3217', name: 'Kết cấu tính toán ô tô' },
    { code: 'AET3218', name: 'Cấu tạo ô tô' }
  ]

  useEffect(() => {
    setResults(sampleResults)
    setFilteredResults(sampleResults)
  }, [])

  useEffect(() => {
    let filtered = results.filter(result => {
      const matchesSearch = result.document_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        result.student_name.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesCourse = selectedCourse === 'all' || result.course_code === selectedCourse
      return matchesSearch && matchesCourse
    })
    setFilteredResults(filtered)
  }, [results, searchTerm, selectedCourse])

  const getScoreBadge = (score, maxScore = 4.0) => {
    const percentage = (score / maxScore) * 100
    if (percentage >= 87.5) return { label: 'Xuất sắc', color: 'bg-green-100 text-green-800' }
    if (percentage >= 75) return { label: 'Tốt', color: 'bg-blue-100 text-blue-800' }
    if (percentage >= 62.5) return { label: 'Trung bình', color: 'bg-yellow-100 text-yellow-800' }
    return { label: 'Yếu', color: 'bg-red-100 text-red-800' }
  }

  const getConfidenceBadge = (confidence) => {
    if (confidence >= 0.9) return { label: 'Rất cao', color: 'bg-green-100 text-green-800' }
    if (confidence >= 0.8) return { label: 'Cao', color: 'bg-blue-100 text-blue-800' }
    if (confidence >= 0.7) return { label: 'Trung bình', color: 'bg-yellow-100 text-yellow-800' }
    return { label: 'Thấp', color: 'bg-red-100 text-red-800' }
  }

  const handleViewDetail = (result) => {
    setSelectedDocument(result)
    setViewMode('detail')
  }

  const handleExportReport = (result) => {
    // In real implementation, this would generate and download a report
    console.log('Exporting report for:', result.document_name)
  }

  // Prepare data for charts
  const getChartData = () => {
    if (filteredResults.length === 0) return []
    
    const cloData = {}
    filteredResults.forEach(result => {
      result.clo_scores.forEach(clo => {
        if (!cloData[clo.clo_code]) {
          cloData[clo.clo_code] = { name: clo.clo_code, scores: [], title: clo.clo_title }
        }
        cloData[clo.clo_code].scores.push(clo.score)
      })
    })

    return Object.values(cloData).map(clo => ({
      name: clo.name,
      title: clo.title,
      average: clo.scores.reduce((a, b) => a + b, 0) / clo.scores.length,
      count: clo.scores.length
    }))
  }

  const getRadarData = (result) => {
    return result.clo_scores.map(clo => ({
      subject: clo.clo_code,
      score: clo.score,
      fullMark: 4.0
    }))
  }

  if (viewMode === 'detail' && selectedDocument) {
    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <Button variant="outline" onClick={() => setViewMode('list')}>
              ← Quay lại danh sách
            </Button>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" onClick={() => handleExportReport(selectedDocument)}>
              <Download className="w-4 h-4 mr-2" />
              Tải báo cáo
            </Button>
          </div>
        </div>

        {/* Document Info */}
        <Card>
          <CardHeader>
            <CardTitle>Chi tiết kết quả đánh giá</CardTitle>
            <CardDescription>{selectedDocument.document_name}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">Sinh viên</p>
                <p className="font-medium">{selectedDocument.student_name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Môn học</p>
                <p className="font-medium">{selectedDocument.course_code} - {selectedDocument.course_name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Điểm tổng thể</p>
                <div className="flex items-center space-x-2">
                  <span className="text-2xl font-bold">{selectedDocument.overall_score.toFixed(1)}/4.0</span>
                  <Badge className={getScoreBadge(selectedDocument.overall_score).color}>
                    {selectedDocument.achievement_level}
                  </Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* CLO Scores Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Điểm CLO</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={selectedDocument.clo_scores}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="clo_code" />
                  <YAxis domain={[0, 4]} />
                  <Tooltip />
                  <Bar dataKey="score" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Radar Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Biểu đồ radar CLO</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={getRadarData(selectedDocument)}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis domain={[0, 4]} />
                  <Radar
                    name="Điểm số"
                    dataKey="score"
                    stroke="#8884d8"
                    fill="#8884d8"
                    fillOpacity={0.6}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Scores */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* CLO Scores */}
          <Card>
            <CardHeader>
              <CardTitle>Chi tiết điểm CLO</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {selectedDocument.clo_scores.map((clo, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-medium">{clo.clo_code}</h4>
                        <p className="text-sm text-gray-600">{clo.clo_title}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-bold">{clo.score.toFixed(1)}/4.0</div>
                        <Badge className={getScoreBadge(clo.score).color}>
                          {getScoreBadge(clo.score).label}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span>Độ tin cậy:</span>
                      <Badge className={getConfidenceBadge(clo.confidence).color}>
                        {(clo.confidence * 100).toFixed(0)}% - {getConfidenceBadge(clo.confidence).label}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* PLO Scores */}
          <Card>
            <CardHeader>
              <CardTitle>Chi tiết điểm PLO</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {selectedDocument.plo_scores.map((plo, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-medium">{plo.plo_code}</h4>
                        <p className="text-sm text-gray-600">{plo.plo_title}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-bold">{plo.score.toFixed(1)}/4.0</div>
                        <Badge className={getScoreBadge(plo.score).color}>
                          {getScoreBadge(plo.score).label}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span>Độ tin cậy:</span>
                      <Badge className={getConfidenceBadge(plo.confidence).color}>
                        {(plo.confidence * 100).toFixed(0)}% - {getConfidenceBadge(plo.confidence).label}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Kết quả đánh giá</h2>
          <p className="text-gray-600">Xem và phân tích kết quả đánh giá CLO/PLO</p>
        </div>
        <div className="flex space-x-2">
          <Button 
            variant={viewMode === 'list' ? 'default' : 'outline'}
            onClick={() => setViewMode('list')}
          >
            Danh sách
          </Button>
          <Button 
            variant={viewMode === 'analytics' ? 'default' : 'outline'}
            onClick={() => setViewMode('analytics')}
          >
            Phân tích
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Tìm kiếm tài liệu, sinh viên..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={selectedCourse} onValueChange={setSelectedCourse}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Chọn môn học" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tất cả môn học</SelectItem>
            {courses.map((course) => (
              <SelectItem key={course.code} value={course.code}>
                {course.code} - {course.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {viewMode === 'analytics' ? (
        // Analytics View
        <div className="space-y-6">
          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{filteredResults.length}</div>
                  <div className="text-sm text-gray-600">Tổng số đánh giá</div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {filteredResults.length > 0 
                      ? (filteredResults.reduce((sum, r) => sum + r.overall_score, 0) / filteredResults.length).toFixed(1)
                      : '0.0'
                    }
                  </div>
                  <div className="text-sm text-gray-600">Điểm trung bình</div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {filteredResults.filter(r => r.overall_score >= 3.5).length}
                  </div>
                  <div className="text-sm text-gray-600">Đạt xuất sắc</div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {filteredResults.filter(r => r.overall_score < 2.0).length}
                  </div>
                  <div className="text-sm text-gray-600">Cần cải thiện</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* CLO Performance Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Hiệu suất CLO trung bình</CardTitle>
              <CardDescription>
                Điểm trung bình của từng CLO
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={getChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 4]} />
                  <Tooltip 
                    formatter={(value, name) => [value.toFixed(2), 'Điểm trung bình']}
                    labelFormatter={(label) => {
                      const item = getChartData().find(d => d.name === label)
                      return item ? `${label}: ${item.title}` : label
                    }}
                  />
                  <Bar dataKey="average" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>
      ) : (
        // List View
        <Card>
          <CardHeader>
            <CardTitle>Danh sách kết quả</CardTitle>
            <CardDescription>
              {filteredResults.length} kết quả đánh giá
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Tài liệu</TableHead>
                  <TableHead>Sinh viên</TableHead>
                  <TableHead>Môn học</TableHead>
                  <TableHead>Điểm tổng thể</TableHead>
                  <TableHead>Mức độ đạt</TableHead>
                  <TableHead>Ngày đánh giá</TableHead>
                  <TableHead>Thao tác</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredResults.map((result) => (
                  <TableRow key={result.id}>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <FileText className="h-4 w-4 text-blue-500" />
                        <div>
                          <p className="font-medium text-sm">{result.document_name}</p>
                          <p className="text-xs text-gray-500 capitalize">{result.document_type}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <User className="h-4 w-4 text-gray-400" />
                        <span>{result.student_name}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{result.course_code}</div>
                        <div className="text-sm text-gray-500">{result.course_name}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-lg font-bold">{result.overall_score.toFixed(1)}/4.0</div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getScoreBadge(result.overall_score).color}>
                        {result.achievement_level}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-1 text-sm text-gray-500">
                        <Calendar className="h-3 w-3" />
                        <span>{result.upload_date}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleViewDetail(result)}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleExportReport(result)}
                        >
                          <Download className="w-4 h-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default AssessmentResults

