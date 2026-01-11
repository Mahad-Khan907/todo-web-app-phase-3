'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { motion } from 'framer-motion';
import { Mail, Lock, ArrowLeft } from 'lucide-react';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormData = z.infer<typeof loginSchema>;

const LoginPage = () => {
  const { login, user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '' },
  });

  // Redirect only if user is actually logged in
  useEffect(() => {
    if (!authLoading && user) {
      router.push('/dashboard');
    }
  }, [user, authLoading, router]);

  const onSubmit = async (data: LoginFormData) => {
    setError(null);
    setIsSubmitting(true);

    try {
      await login(data.email, data.password);
      // The router push is now exclusively handled by the useEffect hook
      // which reacts to the change in the 'user' state.
    } catch (err: any) {
      console.error('Login page error:', err);
      // Display specific error message from backend if available
      const message = err.response?.data?.detail || 'Invalid email or password';
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Only show the full page loader during the initial auth check
  // NOT during the login form submission
  if (authLoading && !isSubmitting) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <p className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent animate-pulse">
          Loading...
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden flex items-center justify-center">
      <div className="fixed inset-0 bg-gradient-to-br from-blue-900/20 via-black to-indigo-900/20" />
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_center,rgba(30,58,138,0.15),transparent_70%)]" />
      
      <div className="fixed inset-0 pointer-events-none opacity-40">
        <div className="absolute top-20 left-0 w-96 h-96 rounded-full blur-3xl bg-blue-500/20" />
        <div className="absolute bottom-40 right-0 w-80 h-80 rounded-full blur-3xl bg-indigo-600/20" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full blur-3xl bg-cyan-600/10" />
      </div>

      <div className="relative z-10 w-full max-w-md px-6">
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={() => router.push('/')}
          className="flex items-center gap-2 text-cyan-300 hover:text-cyan-200 mb-8 transition"
        >
          <ArrowLeft size={20} />
          Back to Home
        </motion.button>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="relative"
        >
          <div className="absolute -inset-4 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-2xl blur-xl opacity-30" />
          
          <div className="relative bg-black/60 backdrop-blur-2xl rounded-2xl border border-white/20 p-8 sm:p-10 shadow-2xl">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent">
                Welcome Back
              </h2>
              <p className="mt-3 text-white/60">Sign in to your account</p>
            </div>

            <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm text-center font-medium"
                >
                  {error}
                </motion.div>
              )}

              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40" size={20} />
                <input
                  {...register('email')}
                  type="email"
                  placeholder="Email address"
                  className={`w-full pl-12 pr-4 py-4 rounded-xl bg-white/10 border ${
                    errors.email ? 'border-red-500/50' : 'border-white/20'
                  } focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition placeholder:text-white/40`}
                />
                {errors.email && (
                  <p className="mt-2 text-sm text-red-400">{errors.email.message}</p>
                )}
              </div>

              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40" size={20} />
                <input
                  {...register('password')}
                  type="password"
                  placeholder="Password"
                  className={`w-full pl-12 pr-4 py-4 rounded-xl bg-white/10 border ${
                    errors.password ? 'border-red-500/50' : 'border-white/20'
                  } focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 transition placeholder:text-white/40`}
                />
                {errors.password && (
                  <p className="mt-2 text-sm text-red-400">{errors.password.message}</p>
                )}
              </div>

              <div className="text-center">
                <a href="/register" className="text-cyan-300 hover:text-cyan-200 underline transition text-sm">
                  Don't have an account? Register here
                </a>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                disabled={isSubmitting}
                className="w-full py-4 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-700 to-cyan-600 text-white font-bold shadow-2xl shadow-blue-500/40 hover:shadow-blue-500/60 disabled:opacity-70 disabled:cursor-not-allowed transition"
              >
                {isSubmitting ? 'Signing in...' : 'Sign In'}
              </motion.button>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default LoginPage;