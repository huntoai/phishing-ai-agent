import React from 'react';
import * as styles from './Badge.module.css';

const Badge = ({
  children,
  variant = 'default',
  size = 'medium',
  className = '',
  ...props
}) => {
  const variantClass = variant === 'default' ? 'defaultVariant' : variant;
  const badgeClasses = [
    styles.badge,
    styles[variantClass],
    styles[size],
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <span className={badgeClasses} {...props}>
      {children}
    </span>
  );
};

export default Badge;
