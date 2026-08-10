"use client";

import type { ReactNode } from "react";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
type ButtonSize = "sm" | "md" | "lg";

type ButtonProps = {
  children: ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  className?: string;
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  fullWidth?: boolean;
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  disabled = false,
  loading = false,
  onClick,
  type = "button",
  fullWidth = false,
}: ButtonProps) {
  const base = "inline-flex items-center justify-center gap-2 font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

  const variants = {
    primary: "bg-[#397f70] text-white hover:bg-[#2b685b] focus:ring-[#397f70]",
    secondary: "bg-[#eef5f2] text-[#17231f] hover:bg-[#dce8e4] focus:ring-[#397f70]",
    ghost: "bg-transparent text-[#397f70] hover:bg-[#eef5f2] focus:ring-[#397f70]",
    danger: "bg-[#bd5b5b] text-white hover:bg-[#a14a4a] focus:ring-[#bd5b5b]",
  };

  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={[
        base,
        variants[variant],
        sizes[size],
        fullWidth ? "w-full" : "",
        className,
      ].join(" ")}
    >
      {loading ? (
        <span className="flex items-center gap-1.5">
          <span className="dot-loader" />
          {children}
        </span>
      ) : (
        children
      )}
    </button>
  );
}