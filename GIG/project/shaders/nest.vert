attribute vec3 aVertexPosition;
attribute vec3 aVertexNormal;
attribute vec2 aTextureCoord;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform sampler2D heightmap;
varying vec2 vTextureCoord;

void main() {
    vTextureCoord = aTextureCoord;
    vec3 offset = 0.4 * aVertexNormal * texture2D(heightmap, vTextureCoord).b;
    gl_Position = uPMatrix * uMVMatrix * vec4(aVertexPosition + offset, 1.0);
}