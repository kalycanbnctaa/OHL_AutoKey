type ToggleProps = {
  enabled: boolean;
  onChange: (enabled: boolean) => void;
  label?: string;
};

export default function Toggle({ enabled, onChange, label }: ToggleProps) {
  return (
    <label className="toggle-container">
      {label && <span className="toggle-label">{label}</span>}
      <button
        type="button"
        className={`toggle-button ${enabled ? "toggle-on" : "toggle-off"}`}
        onClick={() => onChange(!enabled)}
        role="switch"
        aria-checked={enabled}
      >
        <span className="toggle-thumb" />
      </button>
      <span className="toggle-status">{enabled ? "ON" : "OFF"}</span>
    </label>
  );
}