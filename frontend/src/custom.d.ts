declare module '*.svg' {
  const content: any;
  export default content;
}

declare module '*.png' {
  const content: any;
  export default content;
}


declare module 'jwt-decode' {
    interface DecodedToken {
        exp?: number;
        iat?: number;
        role?: string;
        [key: string]: any;
    }

    // Update to use named export
    export function jwtDecode<T = DecodedToken>(token: string): T;
}

