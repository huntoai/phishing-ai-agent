import React from 'react';
import * as styles from './ProgressBar.module.css';

const ProgressBar = ({
  value = 0,
  max = 100,
  variant = 'primary',
  size = 'medium',
  showLabel = false,
  label,
  className = '',
  ...props
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  const barClasses = [
    styles.progressBar,
    styles[size],
    className,
  ]
    .filter(Boolean)
    .join(' ');

  const fillClasses = [
    styles.progressFill,
    styles[variant],
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={barClasses} {...props}>
      {(showLabel || label) && (
        <div className={styles.labelContainer}>
          <span className={styles.label}>{label || `${Math.round(percentage)}%`}</span>
        </div>
      )}
      <div className={styles.progressTrack}>
        <div
          className={fillClasses}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
