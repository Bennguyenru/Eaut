import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog.jsx'
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table.jsx'
import { 
  Plus, 
  Edit, 
  Trash2, 
  BookOpen, 
  Link,
  Search,
  Download,
  Upload,
  Target
} from 'lucide-react'

const CLOManagement = () => {
  const [clos, setClos] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCLO, setSelectedCLO] = useState(null)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [selectedCourse, setSelectedCourse] = useState('all')

  // Sample CLO data
  const sampleCLOs = [
    {
      id: 1,
      code: 'CLO1',
      course_code: 'ME2252',
      course_name: 'Vẽ kỹ thuật',
      title: 'Hiểu các hệ lực cơ học',
      description: 'Hiểu rõ các hệ lực cơ học, các tiên đề tĩnh học',
      pi_code: 'PI 4.1',
      assessment_level: 'U',
      keywords: ['hệ lực', 'cân bằng lực', 'tiên đề tĩnh học'],
      plo_mappings: [
        { plo_code: 'PLO4', weight: 1.0 }
      ]
    },
    {
      id: 2,
      code: 'CLO2',
      course_code: 'ME2252',
      course_name: 'Vẽ kỹ thuật',
      title: 'Xây dựng mô hình lực',
      description: 'Xây dựng mô hình lực, cân bằng lực để giải quyết bài toán',
      pi_code: 'PI 4.2',
      assessment_level: 'A',
      keywords: ['mô hình lực', 'phương trình cân bằng', 'chuyển động phẳng'],
      plo_mappings: [
        { plo_code: 'PLO4', weight: 1.0 }
      ]
    },
    {
      id: 3,
      code: 'CLO3',
      course_code: 'ME2252',
      course_name: 'Vẽ kỹ thuật',
      title: 'Phân tích và tính toán',
      description: 'Phân tích, tính toán, thiết kế tham số kỹ thuật trong cơ học, tĩnh học, động học',
      pi_code: 'PI 10.1',
      assessment_level: 'A',
      keywords: ['động lực học', 'tham số kỹ thuật', 'tính toán thiết kế'],
      plo_mappings: [
        { plo_code: 'PLO10', weight: 1.0 }
      ]
    },
    {
      id: 4,
      code: 'CLO4',
      course_code: 'ME2252',
      course_name: 'Vẽ kỹ thuật',
      title: 'Thái độ học tập',
      description: 'Có ý thức, thái độ học tập nghiêm túc, tích cực',
      pi_code: 'PI 12.1',
      assessment_level: 'T',
      keywords: ['thái độ học tập', 'ý thức', 'chuyên cần'],
      plo_mappings: [
        { plo_code: 'PLO12', weight: 1.0 }
      ]
    }
  ]

  const courses = [
    { code: 'ME2252', name: 'Vẽ kỹ thuật' },
    { code: 'ME2205', name: 'Cơ học kỹ thuật' },
    { code: 'AET3217', name: 'Kết cấu tính toán ô tô' },
    { code: 'AET3218', name: 'Cấu tạo ô tô' }
  ]

  useEffect(() => {
    setClos(sampleCLOs)
  }, [])

  const filteredCLOs = clos.filter(clo => {
    const matchesSearch = clo.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
      clo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      clo.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      clo.course_name.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesCourse = selectedCourse === 'all' || clo.course_code === selectedCourse
    
    return matchesSearch && matchesCourse
  })

  const handleAddCLO = () => {
    setSelectedCLO(null)
    setIsDialogOpen(true)
  }

  const handleEditCLO = (clo) => {
    setSelectedCLO(clo)
    setIsDialogOpen(true)
  }

  const handleDeleteCLO = (id) => {
    if (confirm('Bạn có chắc chắn muốn xóa CLO này?')) {
      setClos(clos.filter(clo => clo.id !== id))
    }
  }

  const handleSaveCLO = (cloData) => {
    if (selectedCLO) {
      // Update existing CLO
      setClos(clos.map(clo => 
        clo.id === selectedCLO.id ? { ...clo, ...cloData } : clo
      ))
    } else {
      // Add new CLO
      const newCLO = {
        id: Math.max(...clos.map(c => c.id)) + 1,
        ...cloData
      }
      setClos([...clos, newCLO])
    }
    setIsDialogOpen(false)
  }

  const getAssessmentLevelBadge = (level) => {
    const levels = {
      'T': { label: 'Thái độ', color: 'bg-blue-100 text-blue-800' },
      'U': { label: 'Hiểu biết', color: 'bg-green-100 text-green-800' },
      'A': { label: 'Áp dụng', color: 'bg-purple-100 text-purple-800' }
    }
    const levelInfo = levels[level] || { label: level, color: 'bg-gray-100 text-gray-800' }
    return (
      <Badge className={levelInfo.color}>
        {levelInfo.label}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Quản lý CLO</h2>
          <p className="text-gray-600">Course Learning Outcomes - Chuẩn đầu ra môn học</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Upload className="w-4 h-4 mr-2" />
            Import CSV
          </Button>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export CSV
          </Button>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={handleAddCLO}>
                <Plus className="w-4 h-4 mr-2" />
                Thêm CLO
              </Button>
            </DialogTrigger>
            <CLODialog 
              clo={selectedCLO} 
              courses={courses}
              onSave={handleSaveCLO}
              onCancel={() => setIsDialogOpen(false)}
            />
          </Dialog>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Tìm kiếm CLO..."
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

      {/* CLO Table */}
      <Card>
        <CardHeader>
          <CardTitle>Danh sách CLO</CardTitle>
          <CardDescription>
            Tổng số: {filteredCLOs.length} CLO
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Mã CLO</TableHead>
                <TableHead>Môn học</TableHead>
                <TableHead>Tiêu đề</TableHead>
                <TableHead>Mức độ đánh giá</TableHead>
                <TableHead>PLO liên kết</TableHead>
                <TableHead>Thao tác</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredCLOs.map((clo) => (
                <TableRow key={clo.id}>
                  <TableCell className="font-medium">{clo.code}</TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">{clo.course_code}</div>
                      <div className="text-sm text-gray-500">{clo.course_name}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">{clo.title}</div>
                      <div className="text-sm text-gray-500 max-w-xs truncate">
                        {clo.description}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    {getAssessmentLevelBadge(clo.assessment_level)}
                  </TableCell>
                  <TableCell>
                    <div className="flex flex-wrap gap-1">
                      {clo.plo_mappings.map((mapping, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          <Link className="w-3 h-3 mr-1" />
                          {mapping.plo_code}
                        </Badge>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex space-x-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleEditCLO(clo)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDeleteCLO(clo.id)}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{clos.length}</div>
              <div className="text-sm text-gray-600">Tổng số CLO</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {clos.filter(c => c.assessment_level === 'U').length}
              </div>
              <div className="text-sm text-gray-600">Hiểu biết</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {clos.filter(c => c.assessment_level === 'A').length}
              </div>
              <div className="text-sm text-gray-600">Áp dụng</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {clos.filter(c => c.assessment_level === 'T').length}
              </div>
              <div className="text-sm text-gray-600">Thái độ</div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// CLO Dialog Component
const CLODialog = ({ clo, courses, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    code: '',
    course_code: '',
    course_name: '',
    title: '',
    description: '',
    pi_code: '',
    assessment_level: 'U',
    keywords: [],
    plo_mappings: []
  })

  useEffect(() => {
    if (clo) {
      setFormData(clo)
    } else {
      setFormData({
        code: '',
        course_code: '',
        course_name: '',
        title: '',
        description: '',
        pi_code: '',
        assessment_level: 'U',
        keywords: [],
        plo_mappings: []
      })
    }
  }, [clo])

  const handleCourseChange = (courseCode) => {
    const course = courses.find(c => c.code === courseCode)
    setFormData({
      ...formData,
      course_code: courseCode,
      course_name: course ? course.name : ''
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave(formData)
  }

  return (
    <DialogContent className="max-w-3xl">
      <DialogHeader>
        <DialogTitle>
          {clo ? 'Chỉnh sửa CLO' : 'Thêm CLO mới'}
        </DialogTitle>
        <DialogDescription>
          Nhập thông tin chi tiết cho chuẩn đầu ra môn học
        </DialogDescription>
      </DialogHeader>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="code">Mã CLO</Label>
            <Input
              id="code"
              value={formData.code}
              onChange={(e) => setFormData({...formData, code: e.target.value})}
              placeholder="VD: CLO1"
              required
            />
          </div>
          <div>
            <Label htmlFor="course">Môn học</Label>
            <Select value={formData.course_code} onValueChange={handleCourseChange}>
              <SelectTrigger>
                <SelectValue placeholder="Chọn môn học" />
              </SelectTrigger>
              <SelectContent>
                {courses.map((course) => (
                  <SelectItem key={course.code} value={course.code}>
                    {course.code} - {course.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="pi_code">Mã PI</Label>
            <Input
              id="pi_code"
              value={formData.pi_code}
              onChange={(e) => setFormData({...formData, pi_code: e.target.value})}
              placeholder="VD: PI 4.1"
            />
          </div>
          <div>
            <Label htmlFor="assessment_level">Mức độ đánh giá</Label>
            <Select 
              value={formData.assessment_level} 
              onValueChange={(value) => setFormData({...formData, assessment_level: value})}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="T">Thái độ (T)</SelectItem>
                <SelectItem value="U">Hiểu biết (U)</SelectItem>
                <SelectItem value="A">Áp dụng (A)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        
        <div>
          <Label htmlFor="title">Tiêu đề</Label>
          <Input
            id="title"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            placeholder="Tiêu đề ngắn gọn của CLO"
            required
          />
        </div>
        
        <div>
          <Label htmlFor="description">Mô tả chi tiết</Label>
          <Textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            placeholder="Mô tả chi tiết về chuẩn đầu ra này"
            rows={3}
            required
          />
        </div>
        
        <div>
          <Label htmlFor="keywords">Từ khóa (cách nhau bởi dấu phẩy)</Label>
          <Input
            id="keywords"
            value={Array.isArray(formData.keywords) ? formData.keywords.join(', ') : ''}
            onChange={(e) => setFormData({
              ...formData, 
              keywords: e.target.value.split(',').map(s => s.trim()).filter(s => s)
            })}
            placeholder="VD: hệ lực, cân bằng lực, tiên đề tĩnh học"
          />
        </div>
        
        <div className="flex justify-end space-x-2">
          <Button type="button" variant="outline" onClick={onCancel}>
            Hủy
          </Button>
          <Button type="submit">
            {clo ? 'Cập nhật' : 'Thêm mới'}
          </Button>
        </div>
      </form>
    </DialogContent>
  )
}

export default CLOManagement

