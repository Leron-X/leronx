"""Tests for scene graph and composition."""
from leronx.scenes import SceneGraph, Scene, CompositionPlanner

class TestSceneGraph:
    def test_add_scene(self):
        g = SceneGraph()
        g.add_scene(Scene(index=0, start_time=0, end_time=5))
        assert len(g) == 1
        assert g.total_duration == 5

class TestCompositionPlanner:
    def test_plan_basic(self):
        planner = CompositionPlanner()
        graph = planner.plan("Scene 1.\n\nScene 2.\n\nScene 3.", target_duration=30)
        assert len(graph.scenes) >= 1
