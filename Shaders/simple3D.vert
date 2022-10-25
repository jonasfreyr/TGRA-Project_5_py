#version 110

attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform vec4 u_camera_position;

uniform mat4 u_model_matrix;

uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

const int u_NUM_OF_LIGHTS = 10;


uniform vec4 u_light_positions[u_NUM_OF_LIGHTS];
uniform int light_amount;


varying vec4 lights_s[u_NUM_OF_LIGHTS];
varying vec4 lights_h[u_NUM_OF_LIGHTS];
varying vec2 v_uv;
varying vec4 normal_normal;



void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	v_uv = a_uv;


	position = u_model_matrix * position;
	normal = u_model_matrix * normal;

	normal_normal = normalize(normal);

	vec4 s;
	vec4 v;
	for(int i = 0; i < light_amount; i++){
		// Diffuse
		s = u_light_positions[i] - position;

		lights_s[i] = s;

		// Specular
		v = normalize(u_camera_position - position);
		lights_h[i] = normalize(s + v);
	}

	position = u_view_matrix * position;
	position = u_projection_matrix * position;

	gl_Position = position;
}