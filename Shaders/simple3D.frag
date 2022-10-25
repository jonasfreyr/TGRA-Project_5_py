#version 110

uniform sampler2D u_tex01;
uniform sampler2D u_tex02;

uniform float u_using_diffuse_texture;
uniform float u_using_specular_texture;

const float MAX_LIGHT_DIST = 10.0;
const int u_NUM_OF_LIGHTS = 10;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform float u_shininess;
uniform vec4 u_material_ambient;

varying vec4 normal_normal;
varying vec4 lights_s[u_NUM_OF_LIGHTS];
varying vec4 lights_h[u_NUM_OF_LIGHTS];
varying vec2 v_uv;

uniform vec4 u_light_diffuses[u_NUM_OF_LIGHTS];
uniform vec4 u_light_speculars[u_NUM_OF_LIGHTS];
uniform vec4 u_light_ambients[u_NUM_OF_LIGHTS];
uniform float u_light_dists[u_NUM_OF_LIGHTS];
uniform int light_amount;

void main(void)
{
    vec4 material_diffuse = u_material_diffuse;
    vec4 material_specular = u_material_specular;
    vec4 material_ambient = u_material_ambient;
    if (u_using_diffuse_texture == 1.0){
        material_diffuse  *= texture2D(u_tex01, v_uv);
        material_ambient *= texture2D(u_tex01, v_uv);
    }
    if (u_using_specular_texture == 1.0) material_specular *= texture2D(u_tex02, v_uv);

    vec4 color = vec4(0, 0, 0, 0);
    float lambert;
    vec4 diffuse_color = vec4(0, 0, 0, 0);
    float phong;
    vec4 specular_color = vec4(0, 0, 0, 0);
    vec4 ambient_color = vec4(0, 0, 0, 0);
    vec4 normal_normal_normal = normalize(normal_normal);
    for(int i = 0; i < light_amount; i++){
        if (length(lights_s[i]) < u_light_dists[i]){
            // Diffuse
            lambert = max(dot(normal_normal_normal, normalize(lights_s[i])), 0.0);
            diffuse_color = lambert * u_light_diffuses[i] * material_diffuse;

            // Specular
            phong = max(dot(normal_normal_normal, normalize(lights_h[i])), 0.0);
            specular_color =  material_specular * u_light_speculars[i] * pow(phong, u_shininess);

            // Ambient
            ambient_color = u_light_ambients[i] * material_ambient;
            color += diffuse_color + specular_color + ambient_color;

            float a = color.a;
            color *= (1.0 - (length(lights_s[i]) / MAX_LIGHT_DIST));
            color.a = a;
        }

    }

    // color.r = color.r * v_uv.x;

    gl_FragColor = color;
}