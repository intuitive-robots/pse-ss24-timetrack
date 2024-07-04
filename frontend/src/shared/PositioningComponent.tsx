import React, {ReactNode, useEffect, useRef, useState} from 'react';

interface PositioningComponentProps {
    children: ReactNode;
}

const PositioningComponent: React.FC<PositioningComponentProps> = ({ children}) => {
    const ref = useRef<HTMLDivElement>(null);
    const [position, setPosition] = useState({ top: 0, left: 0 });

    useEffect(() => {
        if (ref.current) {
            const rect = ref.current.getBoundingClientRect();
            setPosition({
                top: rect.top + window.scrollY,
                left: rect.left + window.scrollX
            });
        }
    }, [ref.current]);

     return (
        <>
            <div ref={ref} id="referenceElement">Referenzelement</div>
            <div style={{
                position: 'absolute',
                top: `${position.top + 20}px`,
                left: `${position.left}px`
            }}>
                {children}
            </div>
        </>
    );
}

export default PositioningComponent;
