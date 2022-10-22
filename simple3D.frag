uniform sampler2D u_tex01;
uniform sampler2D u_tex02;

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
uniform int light_amount;

void main(void)
{
    vec4 material_diffuse = u_material_diffuse * texture2D(u_tex01, v_uv);
    vec4 material_specular = u_material_specular * texture2D(u_tex02, v_uv);

    vec4 color = vec4(0, 0, 0, 0);
    float lambert;
    vec4 diffuse_color;
    float phong;
    vec4 specular_color;
    vec4 ambient_color;
    for(int i = 0; i < light_amount; i++){
        // Diffuse
        lambert = max(dot(normalize(normal_normal), normalize(lights_s[i])), 0.0);
        diffuse_color = lambert * u_light_diffuses[i] * material_diffuse;

        // Specular
        phong = max(dot(normalize(normal_normal), normalize(lights_h[i])), 0.0);
        specular_color =  material_specular * u_light_speculars[i] * pow(phong, u_shininess);

        // Ambient
        ambient_color = u_light_ambients[i] * u_material_ambient;

        color += diffuse_color + specular_color + ambient_color;
    }

    // color.r = color.r * v_uv.x;

    gl_FragColor = color;
}