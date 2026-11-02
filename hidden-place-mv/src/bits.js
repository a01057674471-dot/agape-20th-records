// Small light pieces shared by the sets
import * as THREE from 'three';
export function glowDisc(r, col = '#ffd590') {   // a soft additive disc of light
  const m = new THREE.Mesh(new THREE.PlaneGeometry(r * 2, r * 2), new THREE.ShaderMaterial({ uniforms: { col: { value: new THREE.Color(col) }, k: { value: 0 } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }',
    fragmentShader: 'varying vec2 vUv; uniform vec3 col; uniform float k; void main(){ float r = length(vUv - .5) * 2.; gl_FragColor = vec4(col * k * (pow(max(0., 1. - r), 2.4) * .8 + pow(max(0., 1. - r * 3.), 2.) * .4), 1.); }' }));
  m.renderOrder = 12; m.userData.set = k => { m.material.uniforms.k.value = k; }; return m;
}
