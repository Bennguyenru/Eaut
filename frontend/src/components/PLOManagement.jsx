import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Label } from '@/components/ui/label.jsx'
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
  Target, 
  FileText,
  Search,
  Download,
  Upload
} from 'lucide-react'

const PLOManagement = () => {
  const [plos, setPlos] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPLO, setSelectedPLO] = useState(null)
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  // Sample PLO data
  const samplePLOs = [
    {
      id: 1,
      code: 'PLO4',
      title: 'Áp dụng kiến thức kỹ thuật',
      description: 'Áp dụng, xây dựng và giải quyết các vấn đề kỹ thuật trong CNKT ô tô',
      category: 'Kiến thức chuyên môn',
      pi_codes: ['PI 4.1', 'PI 4.2']
    },
    {
      id: 2,
      code: 'PLO5',
      title: 'Phân tích dữ liệu kỹ thuật',
      description: 'Thực hành, phân tích, giải thích dữ liệu kỹ thuật',
      category: 'Kỹ năng thực hành',
      pi_codes: ['PI 5.1', 'PI 5.2']
    },
    {
      id: 3,
      code: 'PLO6',
      title: 'Thiết kế và chế tạo',
      description: 'Năng lực tham gia thiết kế, chế tạo, vận hành, bảo trì ô tô',
      category: 'Kỹ năng thiết kế',
      pi_codes: ['PI 6.1', 'PI 6.2', 'PI 6.3']
    },
    {
      id: 4,
      code: 'PLO10',
      title: 'Đọc hiểu bản vẽ kỹ thuật',
      description: 'Đọc hiểu và xây dựng bản vẽ kỹ thuật; khai thác, vận hành, quản lý, bảo trì',
      category: 'Kỹ năng kỹ thuật',
      pi_codes: ['PI 10.1', 'PI 10.2']
    },
    {
      id: 5,
      code: 'PLO12',
      title: 'Phẩm chất đạo đức nghề nghiệp',
      description: 'Phẩm chất đạo đức, nghiên cứu độc lập, thích nghi nghề nghiệp',
      category: 'Thái độ',
      pi_codes: ['PI 12.1', 'PI 12.2']
    }
  ]

  useEffect(() => {
    setPlos(samplePLOs)
  }, [])

  const filteredPLOs = plos.filter(plo =>
    plo.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    plo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    plo.description.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleAddPLO = () => {
    setSelectedPLO(null)
    setIsDialogOpen(true)
  }

  const handleEditPLO = (plo) => {
    setSelectedPLO(plo)
    setIsDialogOpen(true)
  }

  const handleDeletePLO = (id) => {
    if (confirm('Bạn có chắc chắn muốn xóa PLO này?')) {
      setPlos(plos.filter(plo => plo.id !== id))
    }
  }

  const handleSavePLO = (ploData) => {
    if (selectedPLO) {
      // Update existing PLO
      setPlos(plos.map(plo => 
        plo.id === selectedPLO.id ? { ...plo, ...ploData } : plo
      ))
    } else {
      // Add new PLO
      const newPLO = {
        id: Math.max(...plos.map(p => p.id)) + 1,
        ...ploData
      }
      setPlos([...plos, newPLO])
    }
    setIsDialogOpen(false)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Quản lý PLO</h2>
          <p className="text-gray-600">Program Learning Outcomes - Chuẩn đầu ra chương trình</p>
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
              <Button onClick={handleAddPLO}>
                <Plus className="w-4 h-4 mr-2" />
                Thêm PLO
              </Button>
            </DialogTrigger>
            <PLODialog 
              plo={selectedPLO} 
              onSave={handleSavePLO}
              onCancel={() => setIsDialogOpen(false)}
            />
          </Dialog>
        </div>
      </div>

      {/* Search */}
      <div className="flex items-center space-x-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Tìm kiếm PLO..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* PLO Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredPLOs.map((plo) => (
          <Card key={plo.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg">{plo.code}</CardTitle>
                  <CardDescription className="font-medium text-gray-700">
                    {plo.title}
                  </CardDescription>
                </div>
                <div className="flex space-x-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleEditPLO(plo)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeletePLO(plo.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-3">
                {plo.description}
              </p>
              <div className="space-y-2">
                <div>
                  <Badge variant="secondary">{plo.category}</Badge>
                </div>
                <div className="flex flex-wrap gap-1">
                  {plo.pi_codes.map((pi, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {pi}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Summary Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Thống kê PLO</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{plos.length}</div>
              <div className="text-sm text-gray-600">Tổng số PLO</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {plos.filter(p => p.category === 'Kiến thức chuyên môn').length}
              </div>
              <div className="text-sm text-gray-600">Kiến thức chuyên môn</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {plos.filter(p => p.category.includes('Kỹ năng')).length}
              </div>
              <div className="text-sm text-gray-600">Kỹ năng</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {plos.filter(p => p.category === 'Thái độ').length}
              </div>
              <div className="text-sm text-gray-600">Thái độ</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// PLO Dialog Component
const PLODialog = ({ plo, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    code: '',
    title: '',
    description: '',
    category: '',
    pi_codes: []
  })

  useEffect(() => {
    if (plo) {
      setFormData(plo)
    } else {
      setFormData({
        code: '',
        title: '',
        description: '',
        category: '',
        pi_codes: []
      })
    }
  }, [plo])

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave(formData)
  }

  return (
    <DialogContent className="max-w-2xl">
      <DialogHeader>
        <DialogTitle>
          {plo ? 'Chỉnh sửa PLO' : 'Thêm PLO mới'}
        </DialogTitle>
        <DialogDescription>
          Nhập thông tin chi tiết cho chuẩn đầu ra chương trình
        </DialogDescription>
      </DialogHeader>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="code">Mã PLO</Label>
            <Input
              id="code"
              value={formData.code}
              onChange={(e) => setFormData({...formData, code: e.target.value})}
              placeholder="VD: PLO1"
              required
            />
          </div>
          <div>
            <Label htmlFor="category">Danh mục</Label>
            <Input
              id="category"
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
              placeholder="VD: Kiến thức chuyên môn"
              required
            />
          </div>
        </div>
        
        <div>
          <Label htmlFor="title">Tiêu đề</Label>
          <Input
            id="title"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            placeholder="Tiêu đề ngắn gọn của PLO"
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
          <Label htmlFor="pi_codes">Mã PI (cách nhau bởi dấu phẩy)</Label>
          <Input
            id="pi_codes"
            value={Array.isArray(formData.pi_codes) ? formData.pi_codes.join(', ') : ''}
            onChange={(e) => setFormData({
              ...formData, 
              pi_codes: e.target.value.split(',').map(s => s.trim()).filter(s => s)
            })}
            placeholder="VD: PI 4.1, PI 4.2"
          />
        </div>
        
        <div className="flex justify-end space-x-2">
          <Button type="button" variant="outline" onClick={onCancel}>
            Hủy
          </Button>
          <Button type="submit">
            {plo ? 'Cập nhật' : 'Thêm mới'}
          </Button>
        </div>
      </form>
    </DialogContent>
  )
}

export default PLOManagement

