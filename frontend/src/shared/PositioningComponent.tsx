import React, { ReactNode, useEffect, useState } from 'react';

interface PositioningComponentProps {
    children: ReactNode;
    targetClass: string;
}

const PositioningComponent: React.FC<PositioningComponentProps> = ({ children, targetClass }) => {
    const [position, setPosition] = useState({ top: 0, left: 0 });

    useEffect(() => {
        const updatePosition = () => {
            const targetElements = document.getElementsByClassName(targetClass);
            if (targetElements.length > 0) {
                const lastElement = targetElements[targetElements.length - 1] as HTMLElement;
                const rect = lastElement.getBoundingClientRect();
                setPosition({
                    top: rect.top + rect.height + window.scrollY,
                    left: rect.left + window.scrollX
                });
            }
        };

        window.addEventListener('resize', updatePosition);
        window.addEventListener('scroll', updatePosition);
        updatePosition();


        return () => {
            window.removeEventListener('resize', updatePosition);
            window.removeEventListener('scroll', updatePosition);
        };
    }, [targetClass]);

    return (
        <div style={{
            position: 'absolute',
            top: `${position.top + 75}px`,
            left: `${position.left - 12}px`,
            width: 'max-content'
        }}>
            {children}
        </div>
    );
}

export default PositioningComponent;
