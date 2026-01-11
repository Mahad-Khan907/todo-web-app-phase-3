'use client'

import { useState, useEffect, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, Check, X, Calendar, Tag, LayoutGrid, LayoutList, Search, Sparkles, Zap, Target, Clock, MessageSquare } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/chat/ChatInterface';
import FloatingChatButton from '@/components/FloatingChatButton';
import { ConversationProvider } from '@/contexts/ConversationContext';

interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
  priority: 'high' | 'medium' | 'low'
  due_date?: string
  tags?: string[]
  completed_at?: string
}

// Toned-down blue theme
const blueConfig = {
  gradientPrimary: 'from-blue-600 via-indigo-700 to-cyan-600',
  gradientSecondary: 'from-cyan-600 to-blue-700',
  glowPrimary: 'shadow-blue-500/30',
  glowSecondary: 'shadow-cyan-500/30',
  textGlow: 'text-cyan-300',
  borderGlow: 'border-cyan-500/30',
}

const priorityConfig = {
  high: { gradient: 'from-red-500/70 to-orange-500/70', glow: 'shadow-red-500/20' },
  medium: { gradient: 'from-yellow-400/70 to-amber-500/70', glow: 'shadow-yellow-400/20' },
  low: { gradient: 'from-green-400/70 to-emerald-500/70', glow: 'shadow-green-400/20' },
}

export default function Dashboard() {
  return (
    <ConversationProvider>
      <DashboardContent />
    </ConversationProvider>
  );
}

function DashboardContent() {
  const queryClient = useQueryClient();
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState<Task['priority']>('medium')
  const [dueDate, setDueDate] = useState('')
  const [tags, setTags] = useState('')
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [showModal, setShowModal] = useState(false)
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'chat'>('grid')
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState<'all' | 'pending' | 'completed' | 'high' | 'medium' | 'low' | 'date'>('all')

  const { user, logout, loading } = useAuth();
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  // ✅ ERROR FIXED: Added trailing slash to /tasks/
  const { data: tasks = [], isLoading } = useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: async () => {
      const response = await api.get('/tasks/'); 
      return response.data;
    },
    enabled: !!user && !loading,
  });

  // ✅ ERROR FIXED: Added trailing slash to /tasks/
  const createTaskMutation = useMutation({
    mutationFn: async (taskData: Omit<Task, 'id'>) => {
      const response = await api.post('/tasks/', taskData);
      return response.data;
    },
    onMutate: async (newTask) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previousTasks = queryClient.getQueryData<Task[]>(['tasks']);
      const optimisticTask = {
        ...newTask,
        id: Date.now(),
        completed: newTask.completed ?? false,
        completed_at: newTask.completed_at ?? undefined,
      } as Task;
      queryClient.setQueryData(['tasks'], (old: Task[] = []) => [optimisticTask, ...old]);
      return { previousTasks };
    },
    onError: (err, newTask, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks'], context.previousTasks);
      }
    },
    onSuccess: (newTask) => {
      queryClient.setQueryData(['tasks'], (old: Task[] = []) =>
        old.map(task => task.id === newTask.id ? newTask : task)
      );
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // ✅ ERROR FIXED: Added trailing slash to /tasks/${id}/
  const updateTaskMutation = useMutation({
    mutationFn: async ({ id, taskData }: { id: number; taskData: Partial<Task> }) => {
      const response = await api.patch(`/tasks/${id}/`, taskData);
      return response.data;
    },
    onMutate: async ({ id, taskData }) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previousTasks = queryClient.getQueryData<Task[]>(['tasks']);
      queryClient.setQueryData(['tasks'], (old: Task[] = []) =>
        old.map(task => task.id === id ? { ...task, ...taskData } : task)
      );
      return { previousTasks };
    },
    onError: (err, { id, taskData }, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks'], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // ✅ ERROR FIXED: Added trailing slash to /tasks/${id}/
  const deleteTaskMutation = useMutation({
    mutationFn: async (id: number) => {
      const response = await api.delete(`/tasks/${id}/`);
      return id;
    },
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previousTasks = queryClient.getQueryData<Task[]>(['tasks']);
      queryClient.setQueryData(['tasks'], (old: Task[] = []) =>
        old.filter(task => task.id !== id)
      );
      return { previousTasks };
    },
    onError: (err, id, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks'], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // memoized stats and filtered tasks logic remains same...
  const stats = useMemo(() => {
    const total = tasks.length
    const today = new Date();
    const completed = tasks.filter(t => t.completed).length
    const todayCompleted = tasks.filter(t =>
      t.completed && t.completed_at && new Date(t.completed_at).toDateString() === today.toDateString()
    ).length
    const dueSoon = tasks.filter(t => {
      if (!t.due_date || t.completed) return false
      const due = new Date(t.due_date)
      const diff = (due.getTime() - today.getTime()) / (1000*60*60*24)
      return diff >= 0 && diff <= 3
    }).length
    const score = total ? Math.round((completed / total) * 100) : 0
    return { total, completed, todayCompleted, dueSoon, score }
  }, [tasks])

  const filteredTasks = useMemo(() => {
    let filtered = tasks.filter(task => {
      const matchesSearch =
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.tags?.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))

      if (filterType === 'pending') return matchesSearch && !task.completed
      if (filterType === 'completed') return matchesSearch && task.completed
      if (['high', 'medium', 'low'].includes(filterType)) return matchesSearch && task.priority === filterType
      return matchesSearch
    });

    if (filterType === 'date') {
      const today = new Date();
      filtered = filtered.sort((a, b) => {
        const aDue = a.due_date ? new Date(a.due_date).getTime() : Infinity;
        const bDue = b.due_date ? new Date(b.due_date).getTime() : Infinity;
        return Math.abs(aDue - today.getTime()) - Math.abs(bDue - today.getTime());
      });
    }

    return filtered;
  }, [tasks, searchQuery, filterType]);

  const openModal = (task?: Task) => {
    if (task) {
      setEditingTask(task)
      setTitle(task.title)
      setDescription(task.description || '')
      setPriority(task.priority)
      setDueDate(task.due_date || '')
      setTags(task.tags?.join(', ') || '')
    } else {
      setEditingTask(null)
      setTitle('')
      setDescription('')
      setPriority('medium')
      setDueDate('')
      setTags('')
    }
    setShowModal(true)
  }

  const saveTask = async () => {
    if (!title.trim()) return;
    const taskData = {
      title: title.trim(),
      description: description.trim() || undefined,
      priority,
      due_date: dueDate || undefined,
      tags: tags.split(',').map(t => t.trim()).filter(Boolean),
      completed: false,
    };

    if (editingTask) {
      updateTaskMutation.mutate({
        id: editingTask.id,
        taskData
      });
    } else {
      createTaskMutation.mutate(taskData);
    }
    setShowModal(false);
  }

  const toggleComplete = async (id: number) => {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    const updatedTaskData = { completed: !task.completed, completed_at: !task.completed ? new Date().toISOString() : undefined };
    updateTaskMutation.mutate({ id, taskData: updatedTaskData });
  }

  const deleteTask = async (id: number) => {
    deleteTaskMutation.mutate(id);
  }

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <p className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent animate-pulse">
          Loading...
        </p>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <p className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent animate-pulse">
          Redirecting...
        </p>
      </div>
    )
  }

  return (
    <>
      <div className="min-h-screen bg-black text-white relative overflow-hidden">
        <div className="fixed inset-0 bg-gradient-to-br from-blue-900/20 via-black to-indigo-900/20" />
        <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_center,rgba(30,58,138,0.15),transparent_70%)]" />

        <div className="fixed inset-0 pointer-events-none opacity-40">
          <div className="absolute top-20 left-0 w-96 h-96 rounded-full blur-3xl bg-blue-500/20" />
          <div className="absolute bottom-40 right-0 w-80 h-80 rounded-full blur-3xl bg-indigo-600/20" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full blur-3xl bg-cyan-600/10" />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
            <button
              onClick={() => { setTimeout(() => { window.location.replace('/') }, 0) }}
              className="font-bold text-xl text-white hover:text-cyan-300 transition"
            >
              Home
            </button>

            <div className="flex sm:flex-row items-start sm:items-center gap-3 sm:gap-4 w-full sm:w-auto">
              <span className="text-white/90 mt-[10px] md:mt-0 text-sm sm:text-base truncate max-w-full sm:max-w-none">
                Hi, {user.email}
              </span>
              <button
                onClick={handleLogout}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-700 to-cyan-600 font-medium text-white shadow-lg hover:shadow-blue-500/50 transition whitespace-nowrap"
              >
                Logout
              </button>
            </div>
          </div>

          <motion.div initial={{ y: -20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.6 }}>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-100 text-center mb-3 drop-shadow-[0_4px_12px_rgba(255,255,255,0.35)]">
              Dashboard
            </h1>
            <p className="text-center text-white/60">Manage your tasks with deep focus</p>
          </motion.div>

          <div className="flex flex-col sm:flex-row gap-4 max-w-4xl mx-auto mb-10 mt-10">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40" size={20} />
              <input
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Search tasks..."
                className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition"
              />
            </div>
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => openModal()}
              className={`px-8 py-3 rounded-xl bg-gradient-to-r ${blueConfig.gradientPrimary} font-semibold text-white flex items-center justify-center gap-2 shadow-lg ${blueConfig.glowPrimary}`}
            >
              <Plus size={20} />
              Add Task
            </motion.button>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
            {[ 
              { icon: Sparkles, label: "Productivity", value: `${stats.score}%`, color: "from-blue-500 to-cyan-500" },
              { icon: Zap, label: "Today", value: stats.todayCompleted, color: "from-indigo-400 to-blue-500" },
              { icon: Target, label: "Active", value: tasks.length - tasks.filter(t=>t.completed).length, color: "from-cyan-400 to-blue-600" },
              { icon: Clock, label: "Due Soon", value: stats.dueSoon, color: "from-blue-400 to-indigo-500" },
            ].map((stat, i) => (
              <motion.div
                key={i}
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
                className="p-5 rounded-2xl bg-white/5 backdrop-blur-md border border-white/10 hover:border-blue-500/30 transition"
              >
                <div className={`h-1 w-full rounded-full bg-gradient-to-r ${stat.color} opacity-40 mb-4`} />
                <stat.icon className="w-8 h-8 mb-3 text-white/70" />
                <p className="text-3xl font-bold text-cyan-300">{stat.value}</p>
                <p className="text-white/50 text-sm mt-1">{stat.label}</p>
              </motion.div>
            ))}
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 mb-8">
            <div className="flex bg-white/5 backdrop-blur-md rounded-xl p-1 border border-white/10">
              <button onClick={() => setViewMode('grid')} className={`p-2.5 rounded-lg transition ${viewMode === 'grid' ? 'bg-white text-black' : 'text-white/60'}`}>
                <LayoutGrid size={18} />
              </button>
              <button onClick={() => setViewMode('list')} className={`p-2.5 rounded-lg transition ${viewMode === 'list' ? 'bg-white text-black' : 'text-white/60'}`}>
                <LayoutList size={18} />
              </button>
              <button onClick={() => setViewMode('chat')} className={`p-2.5 rounded-lg transition ${viewMode === 'chat' ? 'bg-white text-black' : 'text-white/60'}`}>
                <MessageSquare size={18} />
              </button>
            </div>
            {viewMode !== 'chat' && ['all', 'pending', 'completed', 'high', 'medium', 'low', 'date'].map(f => (
              <button
                key={f}
                onClick={() => setFilterType(f as any)}
                className={`px-4 py-2 rounded-lg text-sm capitalize transition ${
                  filterType === f
                    ? `bg-gradient-to-r ${blueConfig.gradientPrimary} text-white font-medium shadow-md`
                    : 'bg-white/5 text-white/60 hover:text-white'
                }`}
              >
                {f === 'all' ? 'All Tasks' : f === 'date' ? 'By Date' : f}
              </button>
            ))}
          </div>

          {viewMode === 'chat' ? (
            <div className="h-[600px]"><ChatInterface onTaskChange={() => queryClient.invalidateQueries({ queryKey: ['tasks'] })} /></div>
          ) : (
            <motion.div layout className={viewMode === 'grid' ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6' : 'space-y-6 max-w-5xl mx-auto'}>
              <AnimatePresence>
                {filteredTasks.length === 0 ? (
                  <p className="col-span-full text-center text-white/40 py-12 text-lg">
                    No tasks found. Create one to get started!
                  </p>
                ) : (
                  filteredTasks.map((task) => (
                    <motion.div
                      key={task.id}
                      layout
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      whileHover={{ y: -4 }}
                      transition={{ duration: 0.3 }}
                      className="relative group"
                    >
                    <div className={`absolute -inset-1.5 bg-gradient-to-r ${priorityConfig[task.priority].gradient} rounded-2xl blur-lg opacity-20 group-hover:opacity-40 transition duration-500`} />
                      <div className="relative bg-black/60 backdrop-blur-xl rounded-2xl border border-white/20 p-6 hover:border-blue-500/40 transition">
                        <div className="flex items-start justify-between mb-4">
                          <motion.button
                            whileTap={{ scale: 0.9 }}
                            onClick={() => toggleComplete(task.id)}
                            className={`w-9 h-9 rounded-full border-2 flex items-center justify-center transition ${
                              task.completed ? `bg-gradient-to-r ${blueConfig.gradientPrimary} border-transparent shadow-md` : 'border-white/40'
                            }`}
                          >
                            {task.completed && <Check size={18} className="text-white" />}
                          </motion.button>
                          <div className="flex gap-3">
                            <motion.button
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.9 }}
                              onClick={() => {
                                if (confirm("Are you sure you want to delete this task?")) {
                                  deleteTask(task.id);
                                }
                              }}
                            >
                              <X size={20} className="text-red-400" />
                            </motion.button>
                            <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} onClick={() => openModal(task)}>
                              <Plus size={20} className="text-cyan-300" />
                            </motion.button>
                          </div>
                        </div>
                        <h3 className={`text-xl font-semibold mb-3 ${task.completed ? 'line-through opacity-60' : ''}`}>
                          {task.title}
                        </h3>
                        {task.description && <p className="text-white/60 text-sm mb-4 break-words">{task.description}</p>}
                        {task.tags && task.tags.length > 0 && (
                          <div className="flex flex-wrap gap-2 mb-5">
                            {task.tags.map((tag, i) => (
                              <span key={i} className="px-3 py-1 rounded-full text-xs bg-white/10 border border-blue-500/20 text-cyan-300">
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                        <div className="flex flex-wrap items-center justify-between gap-3 text-sm">
                          <span className={`font-bold uppercase bg-gradient-to-r ${priorityConfig[task.priority].gradient} bg-clip-text text-transparent`}>
                            {task.priority}
                          </span>
                          {task.due_date && (
                            <span className="flex items-center gap-1 text-white/50">
                              <Calendar size={16} />
                              {new Date(task.due_date).toLocaleDateString()}
                            </span>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}
              </AnimatePresence>
            </motion.div>
          )}
        </div>

        <AnimatePresence>
          {showModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md"
              onClick={() => setShowModal(false)}
            >
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.95, opacity: 0 }}
                transition={{ type: "spring", damping: 25, stiffness: 300 }}
                onClick={e => e.stopPropagation()}
                className="relative w-full max-w-md sm:max-w-lg bg-black/80 backdrop-blur-2xl rounded-2xl border border-blue-500/30 p-6 sm:p-8 shadow-2xl"
              >
                <h2 className="text-2xl sm:text-3xl font-bold mb-6 text-center bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  {editingTask ? 'Edit Task' : 'New Task'}
                </h2>
                <div className="space-y-5">
                  <input
                    placeholder="Title *"
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                    className="w-full px-5 py-4 rounded-xl bg-white/10 border border-white/20 focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition"
                  />
                  <textarea
                    placeholder="Description (optional)"
                    value={description}
                    onChange={e => setDescription(e.target.value)}
                    rows={4}
                    className="w-full px-5 py-4 rounded-xl bg-white/10 border border-white/20 focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 resize-none transition"
                  />
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <input
                      type="date"
                      value={dueDate}
                      onChange={e => setDueDate(e.target.value)}
                      className="px-5 py-4 rounded-xl bg-white/10 border border-white/20 focus:border-cyan-500 focus:outline-none transition"
                    />
                    <div className="grid grid-cols-3 gap-3">
                      {(['low', 'medium', 'high'] as const).map(p => (
                        <button
                          key={p}
                          onClick={() => setPriority(p)}
                          className={`py-3 rounded-xl font-semibold capitalize transition ${
                            priority === p
                              ? `bg-gradient-to-r ${priorityConfig[p].gradient} text-white shadow-md`
                              : 'bg-white/10 text-white/70 hover:text-white'
                          }`}
                        >
                          {p}
                        </button>
                      ))}
                    </div>
                  </div>
                  <input
                    placeholder="Tags (comma separated)"
                    value={tags}
                    onChange={e => setTags(e.target.value)}
                    className="w-full px-5 py-4 rounded-xl bg-white/10 border border-white/20 focus:border-cyan-500 focus:outline-none focus:ring-4 focus:ring-cyan-500/20 transition"
                  />
                </div>
                <div className="flex flex-col sm:flex-row justify-end gap-4 mt-8">
                  <button
                    onClick={() => setShowModal(false)}
                    className="px-8 py-3 cursor-pointer rounded-xl bg-white/10 hover:bg-white/20 transition"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={saveTask}
                    className={`px-10 py-3 rounded-xl bg-gradient-to-r ${blueConfig.gradientPrimary} text-white font-bold cursor-pointer shadow-lg`}
                  >
                    {editingTask ? 'Save Changes' : 'Create Task'}
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      <FloatingChatButton user={user} />
    </>
  )
}