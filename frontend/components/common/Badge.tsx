type BadgeVariant = "success" | "warning" | "error" | "info" | "default";

type BadgeProps = {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
};

export default function Badge({
  children,
  variant = "default",
  className = "",
}: BadgeProps) {
  const variants = {
    success: "bg-[#dff0eb] text-[#2b685b]",
    warning: "bg-[#fdf6e3] text-[#9b8650]",
    error: "bg-[#fde8e8] text-[#a14a4a]",
    info: "bg-[#e3edf5] text-[#2b5f7a]",
    default: "bg-[#eef5f2] text-[#66746f]",
  };

  return (
    <span
      className={[
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
        variants[variant],
        className,
      ].join(" ")}
    >
      {children}
    </span>
  );
}