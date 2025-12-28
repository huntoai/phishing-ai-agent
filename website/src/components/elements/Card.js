import React from 'react';
import * as styles from './Card.module.css';

const Card = ({
  children,
  variant = 'glass',
  hover = true,
  padding = 'medium',
  className = '',
  onClick,
  ...props
}) => {
  const cardClasses = [
    styles.card,
    styles[variant],
    styles[`padding-${padding}`],
    hover ? styles.hover : '',
    onClick ? styles.clickable : '',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={cardClasses} onClick={onClick} {...props}>
      {children}
    </div>
  );
};

export default Card;
